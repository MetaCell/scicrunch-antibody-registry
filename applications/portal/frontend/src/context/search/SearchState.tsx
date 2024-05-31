import React, { useState, useEffect } from 'react'
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
  lastUpdate: Date;
  error: boolean;
  antibodyRequestType: string;
  currentPage: number;
}

const SearchState = (props) => {
  const [baseData, setBaseData] = useState({
    total: 0,
    lastupdate: '-',
    error: false
  });
  const [filterModel, setFilterModel] = useState<GridFilterModel>({ items: [] });
  const [sortModel, setSortModel] = useState<GridSortModel>([]);
  const [filterRequestBody, setFilterRequestBody] = useState(null)
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

  useEffect(() => {
    getDataInfo().then((res) => {
      const lastUpdate = new Date(res.lastupdate)
      setBaseData({ total: res.total, lastupdate: lastUpdate.toDateString(), error: false })
    }).catch((err) => {
      setBaseData({ total: 0, lastupdate: '-', error: true })
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

    const filterItems = mapColumnToBackendModel(antibodyFilters.items, modelType.filter);
    antibodyFilters = { ...antibodyFilters, items: filterItems }
    sortmodel = mapColumnToBackendModel(sortmodel, modelType.sort);
    const filterAndSortModelIsEmpty = isFilterAndSortModelEmpty(antibodyFilters, sortmodel)
    const isUserScope = (searchMode === SEARCH_MODES.MY_FILTERED_AND_SEARCHED_ANTIBODIES);
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
        searchState, antibodyFilters, pageNumber, PAGE_SIZE,
        sortmodel || sortModel, query, isUserScope
      );

      if (!checkIfRequestBodyIsSame(requestBody, filterRequestBody)) {
        fetchFilteredAndSearchedAntibodies(requestBody, pageNumber, query, sortmodel || sortModel);
        setFilterRequestBody(requestBody);
      }
    } else {
      fetchAllAntibodies(pageNumber);
    }
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
    } catch (error) {
      setSearch({
        ...searchState,
        loader: false,
        totalElements: 0,
        activeSearch: query,
        error: true,
        searchedAntibodies: []
      })
      console.error(error)
    }

  }


  const fetchSearchedAntibodies = async (pageNumber = 1, query: string) => {
    setSearch((prev) => ({
      ...prev,
      loader: true
    }))
    try {
      const filteredAntibodies = await getSearchAntibodies(pageNumber, PAGE_SIZE, query)
      setSearch({
        ...searchState,
        loader: false,
        currentPage: pageNumber ? pageNumber : searchState.currentPage,
        activeSearch: query,
        antibodyRequestType: SEARCH_MODES.SEARCHED_ANTIBODIES,
        totalElements: filteredAntibodies.totalElements,
        searchedAntibodies: filteredAntibodies.items,
        error: false
      })
    } catch (error) {
      setSearch({
        ...searchState,
        loader: false,
        activeSearch: query,
        totalElements: 0,
        searchedAntibodies: [],
        error: true
      })
      console.error(error)
    }

  }

  const fetchUserAntibodies = async (pageNumber = 1) => {
    setSearch((prev) => ({
      ...prev,
      loader: true,
      error: false
    }))
    getUserAntibodies(pageNumber, PAGE_SIZE)
      .then((res) => {
        setSearch({
          ...searchState,
          currentPage: pageNumber ? pageNumber : searchState.currentPage,
          loader: false,
          antibodyRequestType: SEARCH_MODES.MY_ANTIBODIES,
          totalElements: res.totalElements,
          searchedAntibodies: res.items,
          error: false
        });
      })
      .catch((err) => {
        setSearch({
          ...searchState,
          loader: false,
          totalElements: 0,
          searchedAntibodies: [],
          error: true
        });
        console.error(err)
      });
  };

  const fetchAllAntibodies = (pageNumber) => {
    setSearch((prev) => ({
      ...prev,
      loader: true,
      error: false
    }))
    getAntibodies(pageNumber, PAGE_SIZE)
      .then((res) => {
        setSearch({
          ...searchState,
          currentPage: pageNumber ? pageNumber : searchState.currentPage,
          loader: false,
          antibodyRequestType: SEARCH_MODES.ALL_ANTIBODIES,
          totalElements: res.totalElements,
          searchedAntibodies: res.items,
          error: false
        });
      })
      .catch((err) => {
        setSearch({
          ...searchState,
          loader: false,
          totalElements: 0,
          searchedAntibodies: [],
          error: true
        });
        console.error(err)
      });
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
      setCurrentPage,
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