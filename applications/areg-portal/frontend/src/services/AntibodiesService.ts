import { DataObjectSharp } from "@mui/icons-material";
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
  url: string;
  insert_time: string;
  curate_time: string;
  disc_date: string;
}

export function getAntibodies(): Promise<AntibodiesObj[]> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(dataJson);
    }, 2000);
  });
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
