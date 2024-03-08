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
    SearchCriteriaOptions.Contains,
    SearchCriteriaOptions.Equals,
    SearchCriteriaOptions.EndsWith,
    SearchCriteriaOptions.StartsWith,
    SearchCriteriaOptions.IsEmpty,
    SearchCriteriaOptions.IsNotEmpty,
    SearchCriteriaOptions.IsAnyOf
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