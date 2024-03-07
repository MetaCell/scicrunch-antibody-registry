import React, { useState, useEffect } from 'react'
import { getSearchAntibodies, getAntibodies, getUserAntibodies, getFilteredAndSearchedAntibodies } from '../../services/AntibodiesService'
import SearchContext from './SearchContext'
import { getDataInfo } from "../../services/InfoService";
import { SEARCH_MODES, PAGE_SIZE, LIMIT_NUM_RESULTS } from '../../constants/constants';

// MUI
import {
  GridFilterModel, GridSortModel
} from "@mui/x-data-grid";
import { structureFiltersAndSorting } from '../../helpers/antibody';


const SearchState = (props) => {
  const [baseData, setBaseData] = useState({
    total: 0,
    lastupdate: new Date()
  });
  const [filterModel, setFilterModel] = useState<GridFilterModel>({ items: [] });
  const [sortModel, setSortModel] = useState<GridSortModel>([]);
  const [filterRequestBody, setFilterRequestBody] = useState(null)
  const [warningMessage, setWarningMessage] = useState('')

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
    getAntibodyList(searchState.antibodyRequestType, searchState.activeSearch, pageNumber, filterModel, sortModel)
  }


  const getAntibodyList = (
    searchMode = SEARCH_MODES.ALL_ANTIBODIES,
    query = '',
    pageNumber = 1,
    antibodyFilters: GridFilterModel = { items: [] },
    sortmodel = sortModel
  ) => {
    if (searchState.antibodyRequestType !== searchMode) {
      pageNumber = 1;   // start with the first page if search type is changed
    }
    // FIVE Kinds of search: 
    if ((antibodyFilters.items.length === 0) && (query || (searchMode === SEARCH_MODES.SEARCHED_ANTIBODIES))) {
      fetchSearchedAntibodies(pageNumber, query);
    } else if ((antibodyFilters.items.length === 0) && (searchMode === SEARCH_MODES.MY_ANTIBODIES)) {
      fetchUserAntibodies(pageNumber);
    } else if ((antibodyFilters.items.length > 0) || (searchMode === SEARCH_MODES.ALL_FILTERED_AND_SEARCHED_ANTIBODIES)
      || (searchMode === SEARCH_MODES.MY_FILTERED_AND_SEARCHED_ANTIBODIES)
    ) {
      const isUserScope = (searchMode === SEARCH_MODES.MY_FILTERED_AND_SEARCHED_ANTIBODIES);
      const requestBody = structureFiltersAndSorting(
        searchState, antibodyFilters, pageNumber, PAGE_SIZE,
        sortmodel || sortModel, query, isUserScope
      );

      if (!checkIfRequestBodyIsSame(requestBody, filterRequestBody)) {
        fetchFilteredAndSearchedAntibodies(requestBody, pageNumber, query, sortmodel || sortModel);
      }
      setFilterRequestBody(requestBody);
    } else {
      fetchAllAntibodies(pageNumber);
    }
  }

  const checkIfRequestBodyIsSame = (requestBody, filterRequestBody) => {
    if (filterRequestBody === null) { return false }
    return JSON.stringify(requestBody) === JSON.stringify(filterRequestBody)

  }

  const fetchFilteredAndSearchedAntibodies = async (antibodyFilters, pageNumber = 1, query: string, sortmodel) => {
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
        antibodyRequestType: SEARCH_MODES.ALL_FILTERED_AND_SEARCHED_ANTIBODIES,
        totalElements: filteredAntibodies.totalElements,
        searchedAntibodies: filteredAntibodies.items
      })

      // if the totalElement is more than the limit, then sorting is not applied in the Backend. 
      // Hence we show the warning message - saying to narrow down the search to apply sorting. 
      // Show warning only if the user has applied sorting.
      if (filteredAntibodies.totalElements > LIMIT_NUM_RESULTS && sortmodel.length > 0) {
        setWarningMessage("Please narrow down the search or filter to apply sorting.")
      } else {
        setWarningMessage('')
      }
    } catch (error) {
      setSearch({
        ...searchState,
        loader: false,
        activeSearch: '',
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
        activeSearch: '',
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
          activeSearch: '',
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
          activeSearch: '',
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
      setFilterModel,
      setSortModel,
      warningMessage,
      setWarningMessage
    }}>
      {props.children}
    </SearchContext.Provider>
  )
}

export default SearchState