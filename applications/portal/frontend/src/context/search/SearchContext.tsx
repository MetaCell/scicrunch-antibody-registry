import { createContext } from "react";
import { Antibody } from "../../rest";
import { GridFilterModel } from "@mui/x-data-grid/models/gridFilterModel";

export interface SearchCriteriaOptions {
  label: string;
  value: string;
}


export interface SearchContextProps  {
  activeSearch: string;
  setActiveSearch: (search: string) => void;
  searchCriteriaOptions: SearchCriteriaOptions[];
  setSearchCriteriaOptions: (options: SearchCriteriaOptions[]) => void;
  totalElements: number;
  lastUpdate: Date | null;
  error: number | boolean | null;
  warningMessage?: string;
  loader: boolean;
  searchedAntibodies: Antibody[];
  getAntibodyList: (
    searchMode?: string,
    searchString?: string,
    pageNumber?: number,
    filterModel?: GridFilterModel,
    sortModel?: any
  ) => void;
  currentPage: number;
  setCurrentPage: (pageNumber: number) => void;
  clearSearch: () => void;
  filterModel: GridFilterModel;
  setFilterModel: (model: GridFilterModel) => void;
  sortModel: any;
  setSortModel: (model: any) => void;
  setWarningMessage: (message: string) => void;
}

const searchContext = createContext<Partial<SearchContextProps>>({})

export default searchContext