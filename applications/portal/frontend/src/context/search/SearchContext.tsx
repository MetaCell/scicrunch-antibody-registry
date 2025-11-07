import { createContext } from "react";

export interface SearchCriteriaOptions {
  label: string;
  value: string;
}

export interface SearchContextProps {
  activeSearch: string;
  setActiveSearch: (search: string) => void;
  searchCriteriaOptions: SearchCriteriaOptions[];
  setSearchCriteriaOptions: (options: SearchCriteriaOptions[]) => void;
}

const searchContext = createContext<Partial<SearchContextProps>>({})

export default searchContext