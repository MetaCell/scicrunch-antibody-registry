import React, { useState } from 'react'
import { getSearchAtibodies } from '../../services/AntibodiesService'
import SearchContext from './SearchContext'

const SearchState = (props) => {

  const [searchState, setSearch] = useState({
    activeSearch:'',
    totalElements:0,
    searchedAntibodies:[]
  })
  const getFilteredAntibodies = async(query:string) => {
    const _=undefined
    const filteredAntibodies = await getSearchAtibodies(_,_,query)
    setSearch({
      activeSearch:query,
      totalElements: filteredAntibodies.totalElements,
      searchedAntibodies: filteredAntibodies.items
    })
  }

  const clearSearch =() => {
    setSearch({
      activeSearch:'',
      totalElements:0,
      searchedAntibodies:[]
    })
  }

  return (
    <SearchContext.Provider value={{
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