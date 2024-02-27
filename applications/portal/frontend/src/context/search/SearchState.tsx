import React, { useState, useEffect } from 'react'
import { getSearchAntibodies, getAntibodies, getUserAntibodies } from '../../services/AntibodiesService'
import SearchContext from './SearchContext'
import { getDataInfo } from "../../services/InfoService";
import { GET_ANTIBODY_TYPES, PAGE_SIZE } from '../../constants/constants';


const SearchState = (props) => {
  const [baseData, setBaseData] = useState({
    total: 0,
    lastupdate: new Date()
  });


  const [searchState, setSearch] = useState({
    loader:true,
    activeSearch:'',
    antibodyRequestType: GET_ANTIBODY_TYPES.ALL_ANTIBODIES,
    currentPage: 1,
    totalElements:0,
    searchedAntibodies: []
  })

  useEffect(() => {
    getDataInfo().then((res) => 
      setBaseData({ total: res.total, lastupdate: new Date(res.lastupdate) })
    ).catch((err) => {
      console.log("Error: ", err)
    })
  }, [])

  const setCurrentPage = (pageNumber) => {
    getAntibodyList(searchState.antibodyRequestType, searchState.activeSearch, pageNumber)
  }

  const getAntibodyList = (antibodyType = GET_ANTIBODY_TYPES.ALL_ANTIBODIES, query = '', pageNumber = 1) => {
    if (searchState.antibodyRequestType !== antibodyType) {
      pageNumber = 1;   // start with the first page if search type is changed
    }

    // THREE Kinds of search: 
    if (query || antibodyType === GET_ANTIBODY_TYPES.SEARCHED_ANTIBODIES) {
      fetchFilteredAntibodies(pageNumber, query);
    } else if (antibodyType === GET_ANTIBODY_TYPES.MY_ANTIBODIES) {
      fetchUserAntibodies(pageNumber);
    } else {
      fetchAllAntibodies(pageNumber);
    }
  }


  const fetchFilteredAntibodies = async (pageNumber = 1, query: string) => {
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
        antibodyRequestType: GET_ANTIBODY_TYPES.SEARCHED_ANTIBODIES,
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
          antibodyRequestType: GET_ANTIBODY_TYPES.MY_ANTIBODIES,
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
          antibodyRequestType: GET_ANTIBODY_TYPES.ALL_ANTIBODIES,
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
    }}>
      {props.children}
    </SearchContext.Provider>
  )
}

export default SearchState