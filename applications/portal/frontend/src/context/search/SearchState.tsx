import React, { useState, useCallback, useEffect } from 'react'
import { getSearchAntibodies } from '../../services/AntibodiesService'
import SearchContext from './SearchContext'
import { getDataInfo } from "../../services/InfoService";

const SearchState = (props) => {
  const [baseData, setBaseData] = useState({
    total: 0,
    lastupdate: new Date()
  });


  useEffect(() => {
    getDataInfo().then((res) => 
      setBaseData({ total: res.total, lastupdate: new Date(res.lastupdate) })
    ).catch((err) => {
      console.log("Error: ", err)
    })},[]);


  const [searchState, setSearch] = useState({
    loader:false,
    activeSearch:'',
    totalElements:0,
    searchedAntibodies:[]
  })
  const getFilteredAntibodies = async (query:string) => {
    setSearch((prev) => ({
      ...prev,
      loader:true
    }))
    const _=undefined
    try {
      const filteredAntibodies = await getSearchAntibodies(_,_,query)
      setSearch({
        loader:false,
        activeSearch:query,
        totalElements: filteredAntibodies.totalElements,
        searchedAntibodies: filteredAntibodies.items
      })
    } catch (error) {
      setSearch({
        loader:false,
        activeSearch:error,
        totalElements: 0,
        searchedAntibodies: []
      })
    }
  
  }

  const clearSearch =() => {
    setSearch({
      loader:false,
      activeSearch:'',
      totalElements:0,
      searchedAntibodies:[]
    })
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
    }}>
      {props.children}
    </SearchContext.Provider>
  )
}

export default SearchState