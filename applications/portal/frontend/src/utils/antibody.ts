import { Antibody, SearchCriteriaOptions } from "../rest";

export function getProperCitation(a: Antibody) {
  if(!a) {return "ERROR";}
  return a.catalogNum && a.vendorName ? `(${a.vendorName} Cat# ${a?.catalogNum?.split(" (")[0]}, RRID:AB_${a.abId})`: "ERROR";
}

function convertCamelCaseToSpaces(str) {
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
  filterModel.items.forEach((item, index) => {
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