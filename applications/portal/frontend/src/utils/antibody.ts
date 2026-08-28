import { GridColumnVisibilityModel } from "@mui/x-data-grid";
import { Antibody } from "../rest";
import { LIMIT_NUM_RESULTS, modelType } from "../constants/constants";
import * as yup from "yup";

export const SearchCriteriaOptions = {
  Contains: 'contains',
  Equals: 'equals',
  EndsWith: 'endsWith',
  StartsWith: 'startsWith',
  SortOn: 'sortOn',
  IsEmpty: 'isEmpty',
  IsNotEmpty: 'isNotEmpty',
  IsAnyOf: 'isAnyOf',
  Operation: 'operation',
  IsUserScope: 'isUserScope',
  Page: 'page',
  Size: 'size',
  Search: 'search'
} as const;

export function getProperCitation(a: Antibody) {
  if(!a) {return "ERROR";}
  return a.catalogNum && a.vendorName ? `(${a.vendorName} Cat# ${a?.catalogNum?.split(" (")[0]}, RRID:AB_${a.abId})`: "ERROR";
}

function convertCamelCaseToSpaces(str: string) {
  return str.replace(/([A-Z])/g, ' $1').toLowerCase();
}

export function getFilterOperators() {
  const operators = [
    SearchCriteriaOptions.Equals,
    SearchCriteriaOptions.Contains,
    SearchCriteriaOptions.EndsWith,
    SearchCriteriaOptions.StartsWith,
    SearchCriteriaOptions.IsEmpty,
    SearchCriteriaOptions.IsNotEmpty,
    // SearchCriteriaOptions.IsAnyOf,
  ];
  const operatorsMap = {};
  operators.forEach((operator) => {
    operatorsMap[operator] = convertCamelCaseToSpaces(operator);
  });

  return operatorsMap;
}

export function getRandomId() {
  return Math.floor(Math.random() * 1000000);
}

export function checkIfFilterSetExists(model, filterModel) {
  // BEHAVIOR: if the same filterset is already present, simply show 
  // the existing one instead of adding a new one
  let isFilterSetPresent = false;
  filterModel.items.forEach((item) => {
    if (item.columnField === model.items[0].columnField) {
      isFilterSetPresent = true;
    }
  });
  return isFilterSetPresent;
}

export function shouldEmptyFilterValue(filterSet, operation) {
  // if previous operator was isAnyOf and new operator is not isAnyOf then clear the value
  // similarly if previous operator was not isAnyOf and new operator is isAnyOf then clear the value
  const changedFromIsAnyOf = (filterSet.operatorValue === SearchCriteriaOptions.IsAnyOf && operation !== SearchCriteriaOptions.IsAnyOf)
    || (filterSet.operatorValue !== SearchCriteriaOptions.IsAnyOf && operation === SearchCriteriaOptions.IsAnyOf)

  // if newly selected operator is IsEmpty or IsNotEmpty then clear the value
  const changedFromNoInputOperators = (operation === SearchCriteriaOptions.IsEmpty || operation === SearchCriteriaOptions.IsNotEmpty)
  return changedFromIsAnyOf || changedFromNoInputOperators;
}


// a mapper that converts the frontend CamelCase columns to the backend snake_case columns - in the filters - right before API call
export function mapColumnToBackendModel(columnItems, modeltype) {
  const columnMap = {
    "abName": "ab_name",
    "abTarget": "ab_target",
    "abId": "ab_id",
    "cloneId": "clone_id",
    "sourceOrganism": "source_organism",
    "catalogNum": "catalog_num",
    "comments": "comments",
    "accession": "accession",
    "targetSpecies": "species",
    "applications": "applications",
    "clonality": "clonality",
    "vendorName": "vendor",
    "numOfCitation": "citation"
  }
  const newFilters = columnItems.map((filter) => {
    if (modeltype == modelType.filter) {
      return {
        ...filter,
        columnField: columnMap[filter.columnField]
      }
    } else {
      return {
        ...filter,
        field: columnMap[filter.field]
      }
    }
  });
  return newFilters;
}


export const getColumnsToDisplay = (columns) => {
  const showcolList: GridColumnVisibilityModel = {};
  columns.filter((column) => column?.hideable === true).map((column) => {
    showcolList[column.field] = false;
  });
  return showcolList;
}

export const validateCatalogNumber = yup.string().matches(/^[^#]+$/, 'The # character is not allowed in the catalog number').required('Catalog number is required')

export const isFilterAndSortModelEmpty = (filtermodel, sortmodel) => {
  return filtermodel.items.length === 0 && sortmodel.length === 0
}

export const checkIfRequestBodyIsSame = (newRequestBody, prevRequestBody) => {
  if (prevRequestBody === null) { return false }
  return JSON.stringify(newRequestBody) === JSON.stringify(prevRequestBody)
}
/**
 * The backend stops counting search matches once it has seen LIMIT_NUM_RESULTS
 * of them and reports exactly one past that, because counting the rest forces
 * Postgres to visit every matching row -- over a minute on common terms. That
 * one value therefore means "at least this many" and is shown as "10,000+".
 *
 * Tested for equality rather than as a threshold on purpose: the limit is
 * switchable from values.yaml (apps.portal.search_count_limit), and when it is
 * off the backend sends real totals well above LIMIT_NUM_RESULTS that must be
 * shown verbatim. Keep this constant equal to the configured `limit`.
 */
export const isTotalCapped = (totalElements: number) =>
  totalElements === LIMIT_NUM_RESULTS + 1;

export const formatTotalElements = (totalElements: number) =>
  isTotalCapped(totalElements)
    ? `${LIMIT_NUM_RESULTS.toLocaleString("en-US")}+`
    : totalElements.toLocaleString("en-US");

/**
 * The banner shown above the results when the search hit one of the backend's
 * two large-result-set behaviours.
 *
 * They are separate conditions and can both apply at once, so the sentences
 * compose: the cap is an equality on the sentinel total, while sorting is
 * skipped for any result set over LIMIT_NUM_RESULTS whether or not the count
 * itself was capped. Returns "" when neither applies.
 */
export const searchWarningMessage = (
  totalElements: number,
  isSorted: boolean
): string => {
  const sentences: string[] = [];
  if (isTotalCapped(totalElements)) {
    sentences.push(
      `To keep this search fast, we're showing the first ${LIMIT_NUM_RESULTS.toLocaleString(
        "en-US"
      )} matches.`
    );
  }
  if (totalElements > LIMIT_NUM_RESULTS && isSorted) {
    sentences.push("Sorting isn't applied to result sets this large.");
  }
  if (!sentences.length) {
    return "";
  }
  sentences.push(
    "If you don't see what you're looking for, try a more specific search term or add a filter to narrow things down."
  );
  return sentences.join(" ");
};
