import React, { useState } from 'react'
//import { getSearchAtibodies } from '../../services/AntibodiesService'
import { getAntibodies } from '../../services/AntibodiesService'
import SearchContext from './SearchContext'

const SearchState = (props) => {

  const [searchState, setSearch] = useState({
    activeSearch:false,
    searchedAntibodies:[]
  })
  const getFilteredAntibodies = async(query:string) => {

    //const filteredAntibodies = await getSearchAtibodies(query)
    const all = await getAntibodies()
    const filteredAntibodies = all.items.filter((ele) => ele.catalogNum.includes(query))
    setSearch({
      activeSearch:true,
      searchedAntibodies: filteredAntibodies
    })
  }

  const clearSearch =() => {
    setSearch({
      activeSearch:false,
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