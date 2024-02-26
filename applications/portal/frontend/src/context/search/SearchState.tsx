import React, { useState, useEffect } from 'react'
import { getSearchAntibodies, getAntibodies } from '../../services/AntibodiesService'
import SearchContext from './SearchContext'
import { getDataInfo } from "../../services/InfoService";
import { PAGE_SIZE } from '../../constants/constants';

const SearchState = (props) => {
  const [baseData, setBaseData] = useState({
    total: 0,
    lastupdate: new Date()
  });

  const searchParams = new URLSearchParams(window.location.search);
  const query = searchParams.get('q');

  const [searchState, setSearch] = useState({
    loader:true,
    activeSearch:'',
    currentPage: 1,
    totalElements:0,
    searchedAntibodies:[]
  })

  useEffect(() => {
    getDataInfo().then((res) => 
      setBaseData({ total: res.total, lastupdate: new Date(res.lastupdate) })
    ).catch((err) => {
      console.log("Error: ", err)
    })

    fetchAntibodies()
  }, [])

  const fetchAntibodies = (pageNumber = 1) => {
    if (query) {
      getFilteredAntibodies(query);
    } else {
      getAntibodies(pageNumber, PAGE_SIZE)
        .then((res) => {
          setSearch({
            ...searchState,
            currentPage: pageNumber ? pageNumber : searchState.currentPage,
            loader: false,
            activeSearch: "",
            totalElements: res.totalElements,
            searchedAntibodies: res.items,
          });
        })
        .catch((err) => console.error(err));
    }
  }

  const setCurrentPage = (pageNumber) => {
    fetchAntibodies(pageNumber)
  }

  const setTotalElements = (total) => {
    setSearch({
      ...searchState,
      totalElements: total
    })
  }

  const getFilteredAntibodies = async (query:string) => {
    setSearch((prev) => ({
      ...prev,
      loader:true
    }))
    const _=undefined
    try {
      const filteredAntibodies = await getSearchAntibodies(_,_,query)
      setSearch({
        ...searchState,
        loader:false,
        activeSearch:query,
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
    }
  
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
      totalElements: searchState.activeSearch ? searchState.totalElements: baseData.total,
      lastUpdate: baseData.lastupdate,
      getFilteredAntibodies,
      clearSearch,
      currentPage: searchState.currentPage,
      setCurrentPage,
      setTotalElements,
    }}>
      {props.children}
    </SearchContext.Provider>
  )
}

export default SearchState