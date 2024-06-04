import { Antibody } from "../rest";
import { addAntibody } from "../services/AntibodiesService";
import { FilterRequest, FilterRequestOperationEnum, KeyValueArrayPair, KeyValuePair, SearchCriteriaOptions } from '../rest';

export function postNewAntibody(
  a: Antibody,
  setAntibodyId: (id: string) => void,
  setApiResponse: (obj: {}) => void,
  next: () => void
) {
  addAntibody(a)
    .then((res) => {
      setAntibodyId(res.abId);
      setApiResponse({ status: 200, detail: res.abId });
      next();
    })
    .catch((err) => {
      const { status, data } = err.response;
      if (status === 409) {
        setApiResponse({
          status: 409,
          detail: data.abId,
        });
        setAntibodyId(data.abId);
      } else {
        setApiResponse({
          status,
          detail: data.detail,
        });
      }
      next();
    });
}


export const structureFiltersAndSorting = (searchState, antibodyFilters, pagenumber, size, sortmodel, newsearch, isUserScope) => {
  let body: FilterRequest = {
    search: newsearch,
    contains: [],
    equals: [],
    startsWith: [],
    endsWith: [],
    isEmpty: [],
    isNotEmpty: [],
    isAnyOf: [],
    page: pagenumber,
    size: size,
    sortOn: [],
    operation: FilterRequestOperationEnum.And,
    isUserScope: isUserScope
  };
  // sort model to be added in the sort
  if (sortmodel && sortmodel.length > 0) {
    body.sortOn = [{
      key: sortmodel[0].field,
      sortorder: sortmodel[0].sort
    }]
  }

  if (antibodyFilters.items && antibodyFilters.items.length > 0) {
    const filterMapper = {
      [SearchCriteriaOptions.Contains]: 'contains',
      [SearchCriteriaOptions.Equals]: 'equals',
      [SearchCriteriaOptions.StartsWith]: 'startsWith',
      [SearchCriteriaOptions.EndsWith]: 'endsWith',
      [SearchCriteriaOptions.IsEmpty]: 'isEmpty',
      [SearchCriteriaOptions.IsNotEmpty]: 'isNotEmpty',
      [SearchCriteriaOptions.IsAnyOf]: 'isAnyOf'
    }

    antibodyFilters.items.map((filter) => {
      const keyval: KeyValuePair = {
        key: filter.columnField,
        value: filter?.value
      }
      const keyvalarr: KeyValueArrayPair = {
        key: filter.columnField,
        value: filter?.value
      }

      if (filter.operatorValue === SearchCriteriaOptions.IsEmpty || filter.operatorValue === SearchCriteriaOptions.IsNotEmpty) {
        body[filterMapper[filter.operatorValue]].push(filter.columnField)
      } else {
        if (filter?.value) {
          const keyvalpair = (filter.operatorValue === SearchCriteriaOptions.IsAnyOf) ? keyvalarr : keyval
          body[filterMapper[filter.operatorValue]].push(keyvalpair)
        }
      }
    })
  }
  return body;
}