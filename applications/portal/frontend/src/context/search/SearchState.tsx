import React, { useState } from 'react'
import { getSearchAtibodies } from '../../services/AntibodiesService'
import SearchContext from './SearchContext'

const SearchState = (props) => {

  const [searchState, setSearch] = useState({
    activeSearch:'',
    searchedAntibodies:[]
  })
  const getFilteredAntibodies = async(query:string) => {
    const _=undefined
    const filteredAntibodies = await getSearchAtibodies(_,_,query)
    setSearch({
      activeSearch:query,
      searchedAntibodies: filteredAntibodies.items
    })
  }

  const clearSearch =() => {
    setSearch({
      activeSearch:'',
      searchedAntibodies:[]
    })
  }

  return (
    <SearchContext.Provider value={{
      activeSearch: searchState.activeSearch,
      searchedAntibodies: searchState.searchedAntibodies,
      getFilteredAntibodies,
      clearSearch,
    }}>
      {props.children}
    </SearchContext.Provider>
  )
}

export default SearchState