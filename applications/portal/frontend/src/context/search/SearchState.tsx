import React, { useState, useEffect } from 'react'
import { getSearchAntibodies, getAntibodies, getUserAntibodies, getFilteredAndSearchedAntibodies } from '../../services/AntibodiesService'
import SearchContext from './SearchContext'
import { getDataInfo } from "../../services/InfoService";
import { SEARCH_MODES, PAGE_SIZE } from '../../constants/constants';
import { FilterRequest, KeyValueArrayPair, KeyValuePair } from '../../rest';

// MUI
import {
  GridFilterModel,
} from "@mui/x-data-grid";


const SearchState = (props) => {
  const [baseData, setBaseData] = useState({
    total: 0,
    lastupdate: new Date()
  });
  const [filterModel, setFilterModel] = useState<GridFilterModel>({ items: [] });
  const [filterRequestBody, setFilterRequestBody] = useState(null)

  const [searchState, setSearch] = useState({
    loader:true,
    activeSearch:'',
    antibodyRequestType: SEARCH_MODES.ALL_ANTIBODIES,
    currentPage: 1,
    totalElements:0,
    searchedAntibodies: []
  })

  useEffect(() => {
    getDataInfo().then((res) => 
      setBaseData({ total: res.total, lastupdate: new Date(res.lastupdate) })
    ).catch((err) => {
      console.error("Error: ", err)
    })
  }, [])

  const setCurrentPage = (pageNumber) => {
    getAntibodyList(searchState.antibodyRequestType, searchState.activeSearch, pageNumber)
  }

  const structureFiltersAndSorting = (antibodyFilters, pagenumber, size) => {
    let body: FilterRequest = {
      search: searchState.activeSearch,
      contains: [],
      equals: [],
      startsWith: [],
      endsWith: [],
      isEmpty: [],
      isNotEmpty: [],
      isAnyOf: [],
      page: pagenumber,
      size: size
    };

    if (antibodyFilters.items && antibodyFilters.items.length > 0) {
      antibodyFilters.items.map((filter) => {

        // I don't like this check below... maybe more standardized
        if (filter.operatorValue === "contains"
          || filter.operatorValue === "equals"
          || filter.operatorValue === "startsWith"
          || filter.operatorValue === "endsWith"
        ) {
          const keyval: KeyValuePair = {
            key: filter.columnField,
            value: filter.value
          }
          if (filter?.value) {
            filter.operatorValue === "contains" ?
              body.contains.push(keyval) :
              filter.operatorValue === "equals" ?
                body.equals.push(keyval) :
                filter.operatorValue === "startsWith" ?
                  body.startsWith.push(keyval) :
                  body.endsWith.push(keyval)
          }

        } else if (filter.operatorValue === "isEmpty"
          || filter.operatorValue === "isNotEmpty"
        ) {
          filter.operatorValue === "isEmpty" ?
            body.isEmpty.push(filter.columnField) :
            body.isNotEmpty.push(filter.columnField)
        } else if (filter.operatorValue === "isAnyOf") {
          const keyval: KeyValueArrayPair = {
            key: filter.columnField,
            value: filter.value
          }
          if (filter?.value) {
            body.isAnyOf.push(keyval)
          }
        }
      })
    }
    return body;
  }

  const getAntibodyList = (searchMode = SEARCH_MODES.ALL_ANTIBODIES, query = '', pageNumber = 1, antibodyFilters = {}) => {
    if (searchState.antibodyRequestType !== searchMode) {
      pageNumber = 1;   // start with the first page if search type is changed
    }
    // FOUR Kinds of search: 
    if (query || (searchMode === SEARCH_MODES.SEARCHED_ANTIBODIES)) {
      fetchSearchedAntibodies(pageNumber, query);
    } else if (searchMode === SEARCH_MODES.MY_ANTIBODIES) {
      fetchUserAntibodies(pageNumber);
    } else if (searchMode === SEARCH_MODES.FILTERED_AND_SEARCHED_ANTIBODIES) {
      const requestBody = structureFiltersAndSorting(antibodyFilters, pageNumber, PAGE_SIZE);

      if (!checkIfRequestBodyIsSame(requestBody, filterRequestBody)) {
        fetchFilteredAndSearchedAntibodies(requestBody, pageNumber, query);
      }
      setFilterRequestBody(requestBody);
    } else {
      fetchAllAntibodies(pageNumber);
    }
  }

  const checkIfRequestBodyIsSame = (requestBody, filterRequestBody) => {
    // Check if a structure like above is same as the previous one
    if (filterRequestBody === null) { return false }
    console.log("requestBody: ", requestBody, "filterRequestBody: ", filterRequestBody)
    let isSame = true;
    Object.keys(requestBody).forEach((key, index) => {
      if (requestBody[key] !== filterRequestBody[key]) {
        isSame = false;
      }
    })
    console.log("isSame: ", isSame)
    return isSame;
  }

  const fetchFilteredAndSearchedAntibodies = async (antibodyFilters, pageNumber = 1, query: string) => {
    setSearch((prev) => ({
      ...prev,
      loader: true
    }))
    try {
      const filteredAntibodies = await getFilteredAndSearchedAntibodies(antibodyFilters)
      setSearch({
        ...searchState,
        loader: false,
        currentPage: pageNumber ? pageNumber : searchState.currentPage,
        activeSearch: query,
        antibodyRequestType: SEARCH_MODES.FILTERED_AND_SEARCHED_ANTIBODIES,
        totalElements: filteredAntibodies.totalElements,
        searchedAntibodies: filteredAntibodies.items
      })
    } catch (error) {
      setSearch({
        ...searchState,
        loader: false,
        activeSearch: error,
        totalElements: 0,
        searchedAntibodies: []
      })
      console.error(error)
    }

  }


  const fetchSearchedAntibodies = async (pageNumber = 1, query: string) => {
    setSearch((prev) => ({
      ...prev,
      loader:true
    }))
    try {
      const filteredAntibodies = await getSearchAntibodies(pageNumber, PAGE_SIZE, query)
      setSearch({
        ...searchState,
        loader:false,
        currentPage: pageNumber ? pageNumber : searchState.currentPage,
        activeSearch:query,
        antibodyRequestType: SEARCH_MODES.SEARCHED_ANTIBODIES,
        totalElements: filteredAntibodies.totalElements,
        searchedAntibodies: filteredAntibodies.items
      })
    } catch (error) {
      setSearch({
        ...searchState,
        loader:false,
        activeSearch:error,
        totalElements: 0,
        searchedAntibodies: []
      })
      console.error(error)
    }
  
  }

  const fetchUserAntibodies = async (pageNumber = 1) => {
    setSearch((prev) => ({
      ...prev,
      loader: true
    }))
    getUserAntibodies(pageNumber, PAGE_SIZE)
      .then((res) => {
        setSearch({
          ...searchState,
          currentPage: pageNumber ? pageNumber : searchState.currentPage,
          loader: false,
          antibodyRequestType: SEARCH_MODES.MY_ANTIBODIES,
          activeSearch: "",
          totalElements: res.totalElements,
          searchedAntibodies: res.items,
        });
      })
      .catch((err) => {
        setSearch({
          ...searchState,
          loader: false,
          totalElements: 0,
          activeSearch: err,
          searchedAntibodies: []
        });
        console.error(err)
      });
  };

  const fetchAllAntibodies = (pageNumber) => {
    setSearch((prev) => ({
      ...prev,
      loader: true
    }))
    getAntibodies(pageNumber, PAGE_SIZE)
      .then((res) => {
        setSearch({
          ...searchState,
          currentPage: pageNumber ? pageNumber : searchState.currentPage,
          loader: false,
          activeSearch: "",
          antibodyRequestType: SEARCH_MODES.ALL_ANTIBODIES,
          totalElements: res.totalElements,
          searchedAntibodies: res.items,
        });
      })
      .catch((err) => {
        setSearch({
          ...searchState,
          loader: false,
          totalElements: 0,
          activeSearch: err,
          searchedAntibodies: []
        });
        console.error(err)
      });
  }

  const clearSearch =() => {
    setSearch({
      ...searchState,
      loader:true,
      activeSearch:'',
      totalElements:0,
      searchedAntibodies:[]
    })
    getAntibodies()
      .then((res) => {
        setSearch({
          ...searchState,
          loader:false,
          activeSearch: "",
          totalElements: res.totalElements,
          searchedAntibodies: res.items
        })
      })
      .catch((err) => console.error(err))
  }

  return (
    <SearchContext.Provider value={{
      loader: searchState.loader,
      activeSearch: searchState.activeSearch,
      searchedAntibodies: searchState.searchedAntibodies,
      totalElements: searchState.totalElements,
      lastUpdate: baseData.lastupdate,
      getAntibodyList,
      clearSearch,
      currentPage: searchState.currentPage,
      setCurrentPage,
      filterModel,
      setFilterModel
    }}>
      {props.children}
    </SearchContext.Provider>
  )
}

export default SearchState