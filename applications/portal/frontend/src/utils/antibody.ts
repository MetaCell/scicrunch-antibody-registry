import { Antibody } from "../rest";

export function getProperCitation(a: Antibody) {
  return `(${a.vendorName}#${a.catalogNum}, RRID:AB_${a.abId})`;
}
