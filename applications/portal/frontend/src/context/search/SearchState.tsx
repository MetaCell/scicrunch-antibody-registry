import React, { useState, useEffect, useCallback } from 'react'
import { getSearchAntibodies, getAntibodies, getUserAntibodies, getFilteredAndSearchedAntibodies } from '../../services/AntibodiesService'
import SearchContext from './SearchContext'
import { getDataInfo } from "../../services/InfoService";
import { SEARCH_MODES, PAGE_SIZE, LIMIT_NUM_RESULTS, modelType } from '../../constants/constants';

// MUI
import {
  GridFilterModel, GridSortModel
} from "@mui/x-data-grid";
import { structureFiltersAndSorting } from '../../helpers/antibody';
import { Antibody } from '../../rest';
import { checkIfRequestBodyIsSame, isFilterAndSortModelEmpty, mapColumnToBackendModel } from '../../utils/antibody';

export interface SearchResult {
  loader: boolean;
  activeSearch: string;
  searchedAntibodies: Antibody[];
  totalElements: number;
  lastUpdate: Date | null;
  error: boolean | number;
  antibodyRequestType: string;
  currentPage: number;
}

const SearchState = (props) => {
  const [baseData, setBaseData] = useState<{
    total: number;
    lastupdate: Date | null;
    error: boolean | number;
  }>({
    total: 0,
    lastupdate: null,
    error: false
  });
  const [filterModel, setFilterModel] = useState<GridFilterModel>({ items: [] });
  const [sortModel, setSortModel] = useState<GridSortModel>([]);
  const [filterRequestBody, setFilterRequestBody] = useState<any>(null)
  const [warningMessage, setWarningMessage] = useState('')

  const [searchState, setSearch] = useState<SearchResult>({
    loader: false,
    activeSearch: '',
    antibodyRequestType: SEARCH_MODES.ALL_ANTIBODIES,
    currentPage: 1,
    totalElements: 0,
    searchedAntibodies: [],
    error: false,
    lastUpdate: null
  })

  const setActiveSearch = (searchString) => {
    setSearch((prev) => ({
      ...prev,
      activeSearch: searchString
    }))
  }

  useEffect(() => {
    getDataInfo().then((res) => {
      const lastUpdate = new Date(res.lastupdate)
      setBaseData({ total: res.total, lastupdate: lastUpdate, error: false })
    }).catch((err) => {
      setBaseData({ total: 0, lastupdate: null, error: err?.response?.status ?? true })
      console.error("Error: ", err)
    })
  }, [])

  const setCurrentPage = (pageNumber) => {
    getAntibodyList(searchState.antibodyRequestType, searchState.activeSearch, pageNumber, filterModel, sortModel)
  }

  const searchStateRef = React.useRef(searchState);
  searchStateRef.current = searchState;

  const sortModelRef = React.useRef(sortModel);
  sortModelRef.current = sortModel;
  


  const fetchFilteredAndSearchedAntibodies = useCallback(async (antibodyFilters, pageNumber = 1, query: string, sortmodel) => {
    setSearch((prev) => ({
      ...prev,
      loader: true
    }))
    try {
      const filteredAntibodies = await getFilteredAndSearchedAntibodies(antibodyFilters)
      setSearch({
        ...searchStateRef.current,
        loader: false,
        currentPage: pageNumber ? pageNumber : searchStateRef.current.currentPage,
        activeSearch: query,
        antibodyRequestType: SEARCH_MODES.ALL_FILTERED_AND_SEARCHED_ANTIBODIES,
        totalElements: filteredAntibodies.totalElements,
        searchedAntibodies: filteredAntibodies.items,
        error: false
      })

      // if the totalElement is more than the limit, then sorting is not applied in the Backend. 
      // Hence we show the warning message - saying to narrow down the search to apply sorting. 
      // Show warning only if the user has applied sorting.
      if (filteredAntibodies.totalElements > LIMIT_NUM_RESULTS && sortmodel.length > 0) {
        setWarningMessage("Please narrow down the search or filter to apply sorting.")
      } else {
        setWarningMessage('')
      }
    } catch (error: any) {
      setSearch({
        ...searchStateRef.current,
        loader: false,
        totalElements: 0,
        activeSearch: query,
        error: error?.response?.status ?? true ,
        searchedAntibodies: []
      })
      console.error(error)
    }
  }, [setWarningMessage]);

  const fetchSearchedAntibodies = useCallback(async (pageNumber = 1, query: string) => {
    setSearch((prev) => ({
      ...prev,
      loader: true
    }))
    try {
      const filteredAntibodies = await getSearchAntibodies(pageNumber, PAGE_SIZE, query)
      setSearch({
        ...searchStateRef.current,
        loader: false,
        currentPage: pageNumber ? pageNumber : searchStateRef.current.currentPage,
        activeSearch: query,
        antibodyRequestType: SEARCH_MODES.SEARCHED_ANTIBODIES,
        totalElements: filteredAntibodies.totalElements,
        searchedAntibodies: filteredAntibodies.items,
        error: false
      })
    } catch (error: any) {
      setSearch({
        ...searchStateRef.current,
        loader: false,
        activeSearch: query,
        totalElements: 0,
        searchedAntibodies: [],
        error: error?.response?.status ?? true 
      })
      console.error(error)
    }

  }, []);

  const fetchUserAntibodies = useCallback(async (pageNumber = 1) => {
    setSearch((prev) => ({
      ...prev,
      loader: true,
      error: false
    }))
    getUserAntibodies(pageNumber, PAGE_SIZE)
      .then((res) => {
        setSearch({
          ...searchStateRef.current,
          currentPage: pageNumber ? pageNumber : searchStateRef.current.currentPage,
          loader: false,
          activeSearch: '',
          antibodyRequestType: SEARCH_MODES.MY_ANTIBODIES,
          totalElements: res.totalElements,
          searchedAntibodies: res.items,
          error: false
        });
      })
      .catch((err) => {
        setSearch({
          ...searchStateRef.current,
          loader: false,
          activeSearch: '',
          totalElements: 0,
          searchedAntibodies: [],
          error: true
        });
        console.error(err)
      });
  }, []);



  

  const fetchAllAntibodies = useCallback((pageNumber) => {
    setSearch((prev) => ({
      ...prev,
      loader: true,
      error: false
    }))
    getAntibodies(pageNumber, PAGE_SIZE)
      .then((res) => {
        setSearch({
          ...searchStateRef.current,
          currentPage: pageNumber ? pageNumber : searchStateRef.current.currentPage,
          loader: false,
          antibodyRequestType: SEARCH_MODES.ALL_ANTIBODIES,
          totalElements: res.totalElements,
          searchedAntibodies: res.items,
          error: false
        });
      })
      .catch((err) => {
        setSearch({
          ...searchStateRef.current,
          loader: false,
          totalElements: 0,
          searchedAntibodies: [],
          error: err?.response?.status ?? true 
        });
        console.error(err)
      });
  }, []);


  const getAntibodyList = useCallback((
    searchMode = SEARCH_MODES.ALL_ANTIBODIES,
    query = '',
    pageNumber = 1,
    antibodyFilters: GridFilterModel = { items: [] },
    sortmodel = sortModelRef.current
  ) => {
    if (searchStateRef.current.antibodyRequestType !== searchMode) {
      pageNumber = 1;   // start with the first page if search type is changed
    }

    const filterItems = mapColumnToBackendModel(antibodyFilters.items, modelType.filter);
    antibodyFilters = { ...antibodyFilters, items: filterItems }
    sortmodel = mapColumnToBackendModel(sortmodel, modelType.sort);
    const filterAndSortModelIsEmpty = isFilterAndSortModelEmpty(antibodyFilters, sortmodel)
    const isUserScope = (searchMode === SEARCH_MODES.MY_FILTERED_AND_SEARCHED_ANTIBODIES || searchMode === SEARCH_MODES.MY_ANTIBODIES);
    const isSearchModeFilteredAndSearched = (searchMode === SEARCH_MODES.ALL_FILTERED_AND_SEARCHED_ANTIBODIES) || (searchMode === SEARCH_MODES.MY_FILTERED_AND_SEARCHED_ANTIBODIES);


    // FOUR Kinds of Antibodies fetch:  
    // 1. Search without filters and sorting... pure FTS
    // 2. Get user antibodies - without (filters/sorting or fts)
    // 3. With filters+sorting+fts
    // 4. Get all antibodies - without (filters/sortinng or fts)
    if (filterAndSortModelIsEmpty && (query || (searchMode === SEARCH_MODES.SEARCHED_ANTIBODIES)) && !isUserScope) {
      fetchSearchedAntibodies(pageNumber, query);
    } else if (filterAndSortModelIsEmpty && (searchMode === SEARCH_MODES.MY_ANTIBODIES)) {
      fetchUserAntibodies(pageNumber);
    } else if (!filterAndSortModelIsEmpty || isSearchModeFilteredAndSearched) {
      const requestBody = structureFiltersAndSorting(
        searchStateRef.current, antibodyFilters, pageNumber, PAGE_SIZE,
        sortmodel || sortModelRef.current, query, isUserScope
      );

      if (!checkIfRequestBodyIsSame(requestBody, filterRequestBody)) {
        fetchFilteredAndSearchedAntibodies(requestBody, pageNumber, query, sortmodel || sortModelRef.current);
        setFilterRequestBody(requestBody);
      }
    } else {
      fetchAllAntibodies(pageNumber);
    }
  }, [fetchAllAntibodies, fetchFilteredAndSearchedAntibodies, fetchSearchedAntibodies, fetchUserAntibodies, filterRequestBody]);

  const clearSearch = () => {
    setSearch({
      ...searchState,
      loader: true,
      activeSearch: '',
      totalElements: 0,
      searchedAntibodies: [],
      error: false
    })
    getAntibodies()
      .then((res) => {
        setSearch({
          ...searchState,
          loader: false,
          activeSearch: "",
          totalElements: res.totalElements,
          searchedAntibodies: res.items,
          error: false
        })
      })
      .catch((err) => {
        setSearch({
          ...searchState,
          loader: false,
          totalElements: 0,
          activeSearch: '',
          searchedAntibodies: [],
          error: err?.response?.status ?? true 
        })
        console.error(err)
      })
  }
  return (
    <SearchContext.Provider value={{
      loader: searchState.loader,
      activeSearch: searchState.activeSearch,
      searchedAntibodies: searchState.searchedAntibodies,
      totalElements: searchState.totalElements,
      lastUpdate: baseData.lastupdate,
      error: searchState.error,
      getAntibodyList,
      currentPage: searchState.currentPage,
      setActiveSearch: setActiveSearch,
      setCurrentPage,
      clearSearch,
      filterModel,
      setFilterModel,
      sortModel,
      setSortModel,
      warningMessage,
      setWarningMessage
    }}>
      {props.children}
    </SearchContext.Provider>
  )
}

export default SearchState