import dataJson from "./data.json";

interface AntibodiesObj {
  id: string;
  ab_name: string;
  ab_id: string;
  ab_target: string;
  target_species: string;
  proper_citation: string;
  clonality: string;
  comments: string;
  clone_id: string;
  host: string;
  vendor: string;
  catalog_num?;
}

export function getAntibodies(): Promise<AntibodiesObj[]> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(dataJson);
    }, 2000);
  });
}
