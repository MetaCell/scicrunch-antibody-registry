import React, { useState } from 'react'
import { getSearchAtibodies } from '../../services/AntibodiesService'
import SearchContext from './SearchContext'

const SearchState = (props) => {

  const [searchState, setSearch] = useState({
    loader:false,
    activeSearch:'',
    totalElements:0,
    searchedAntibodies:[]
  })
  const getFilteredAntibodies = async(query:string) => {
    setSearch((prev) => ({
      ...prev,
      loader:true
    }))
    const _=undefined
    try {
      const filteredAntibodies = await getSearchAtibodies(_,_,query)
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
      totalElements: searchState.totalElements,
      getFilteredAntibodies,
      clearSearch,
    }}>
      {props.children}
    </SearchContext.Provider>
  )
}

export default SearchState