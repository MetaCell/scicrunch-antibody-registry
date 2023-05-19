import { Antibody } from "../rest";

export function getProperCitation(a: Antibody) {
  return a.catalogNum && a.vendorName ? `(${a.vendorName} Cat# ${a?.catalogNum?.split(" (")[0]}, RRID:AB_${a.abId})`: "ERROR";
}
