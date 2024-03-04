import { PAGE_SIZE } from "../constants/constants";
import { Configuration } from "../rest";
import {
  Antibody,
  PaginatedAntibodies,
  AntibodyApi,
  AddAntibody,
  AntibodyCommercialTypeEnum,
  SearchApi,
  FilterRequest
} from "../rest/api";

import { getToken } from "./UserService";

const api = new AntibodyApi();
const searchApi = new SearchApi()

export async function getAntibodies(
  page = 1,
  size = 10
): Promise<PaginatedAntibodies> {
  const abs = (await api.getAntibodies(page, size)).data;
  abs.items = abs.items.map(mapAntibody);
  return abs;
}

function mapAntibody(antibody: Antibody): Antibody {
  if((!antibody.showLink || !antibody.url) && antibody.vendorUrl) {
    antibody.url = antibody.vendorUrl[0];
  }
  if (antibody.url && !antibody.url.includes("//")) {
    antibody.url = "https://" + antibody.url;
  }

  return antibody;
}


export async function getAntibody(id: number): Promise<Antibody[]> {
  const abs = await (await api.getAntibody(id)).data;
  return abs.map(mapAntibody);
}

export async function addAntibody(antibodyObj): Promise<any> {
  let ab = mapAntibodyFromForm(antibodyObj);
  return (
    await new AntibodyApi(
      new Configuration({ apiKey: getToken(), accessToken: getToken() })
    ).createAntibody(ab)
  ).data;
}

function mapAntibodyFromForm(antibody): AddAntibody {
  let commercialAb = {
    clonality: antibody.clonality,
    epitope: antibody.epitope,
    comments: antibody.comments,
    url: antibody.url,
    abName: antibody.name,
    abTarget: antibody.antibodyTarget,
    catalogNum: antibody.catalogNumber,
    cloneId: antibody.cloneID,
    commercialType: antibody.type,
    productConjugate: antibody.conjugate,
    productForm: antibody.format,
    productIsotype: antibody.isotype,
    sourceOrganism: antibody.host,
    targetSpecies: antibody.targetSpecies.split(/;,/),
    uniprotId: antibody.uniprotID,
    vendorName: antibody.vendor,
    applications: antibody.applications?.split(/\W/),
  };
  if (antibody.type === AntibodyCommercialTypeEnum.Commercial) {
    return commercialAb;
  } else {
    return {
      ...commercialAb,
      definingCitation: antibody.citation,
    };
  }
}

export async function getUserAntibodies(
  page = 1,
  size = 10
): Promise<PaginatedAntibodies> {
  return (
    await new AntibodyApi(
      new Configuration({ apiKey: getToken(), accessToken: getToken() })
    ).getUserAntibodies(page, size)
  ).data;
}

export async function getSearchAntibodies(
  page = 1,
  size = 10,
  query:string
):Promise<PaginatedAntibodies>{
  const abs = await (
    await searchApi.ftsAntibodies(page, size, query)
  ).data;
  abs.items = abs.items.map(mapAntibody);
  return abs;
}

export async function getFilteredAndSearchedAntibodies(
  filters: FilterRequest = {},
): Promise<PaginatedAntibodies> {
  filters.size = PAGE_SIZE;
  const abs = (
    await searchApi.filterAntibodies(filters)
  ).data;
  abs.items = abs.items.map(mapAntibody);
  return abs;
}

export async function getAntibodyByAccessionNumber(accesionNumber:number){
  return mapAntibody(await (await api.getByAccession(accesionNumber)).data);
}

export async function updateSubmittedAntibody(updatedAntibody, accesionNumber){
  let ab = mapAntibodyFromForm(updatedAntibody);
  delete ab.vendorName 
  delete ab.catalogNum
  return (
    await new AntibodyApi(
      new Configuration({ apiKey: getToken(), accessToken: getToken() })
    ).updateUserAntibody(accesionNumber, ab)
  ).data;
}