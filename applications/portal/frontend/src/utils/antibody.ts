import { Antibody } from "../rest";

export function getProperCitation(a: Antibody) {
  if(!a) {return "ERROR";}
  return a.catalogNum && a.vendorName ? `(${a.vendorName} Cat# ${a?.catalogNum?.split(" (")[0]}, RRID:AB_${a.abId})`: "ERROR";
}

export function getFilterRequestAttributeMap() {
  const filterRequestAttributeMap = {
    'contains': 'contains',
    'equals': 'equals',
    'endsWith': 'ends with',
    'startsWith': 'starts with',
    'isEmpty': 'is empty',
    'isNotEmpty': 'is not empty',
    'isAnyOf': 'is any of',
  }

  return filterRequestAttributeMap;
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