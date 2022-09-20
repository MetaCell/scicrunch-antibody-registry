import { Antibody, PaginatedAntibodies, AntibodyApi } from "../rest/api"
import dataJson from "./data.json";

const api = new AntibodyApi();

export async function getAntibodies(page=0, size=10): Promise<PaginatedAntibodies> {
  return  (await api.getAntibodies(page, size)).data;
}

export function getAntibody(id): Promise<any> {
  let antibody = {};
  for (const ab of dataJson) {
    if (ab.ab_id === id) {
      antibody = ab;
    }
  }
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(antibody);
    }, 1000);
  });
}
