import { Antibody } from "../rest";
import { addAntibody } from "../services/AntibodiesService";
import { FilterRequest, FilterRequestOperationEnum, KeyValueArrayPair, KeyValuePair } from '../rest';

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
    search: newsearch || searchState.activeSearch,
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
    antibodyFilters.items.map((filter) => {
      if (filter.operatorValue === "contains"
        || filter.operatorValue === "equals"
        || filter.operatorValue === "startsWith"
        || filter.operatorValue === "endsWith"
      ) {
        const keyval: KeyValuePair = {
          key: filter.columnField,
          value: filter.value
        }
        if (filter?.value) {
          filter.operatorValue === "contains" ?
            body.contains.push(keyval) :
            filter.operatorValue === "equals" ?
              body.equals.push(keyval) :
              filter.operatorValue === "startsWith" ?
                body.startsWith.push(keyval) :
                body.endsWith.push(keyval)
        }

      } else if (filter.operatorValue === "isEmpty"
        || filter.operatorValue === "isNotEmpty"
      ) {
        filter.operatorValue === "isEmpty" ?
          body.isEmpty.push(filter.columnField) :
          body.isNotEmpty.push(filter.columnField)
      } else if (filter.operatorValue === "isAnyOf") {
        const keyval: KeyValueArrayPair = {
          key: filter.columnField,
          value: filter.value
        }
        if (filter?.value) {
          body.isAnyOf.push(keyval)
        }
      }
    })
  }
  return body;
}