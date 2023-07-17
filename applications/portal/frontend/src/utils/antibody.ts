import { Antibody } from "../rest";

export function getProperCitation(a: Antibody) {
  if(!a) {return "ERROR";}
  return a.catalogNum && a.vendorName ? `(${a.vendorName} Cat# ${a?.catalogNum?.split(" (")[0]}, RRID:AB_${a.abId})`: "ERROR";
}
