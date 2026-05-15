import { PAGE_SIZE } from "../constants/constants";
import { Configuration } from "../rest";
import {
  Antibody,
  PaginatedAntibodies,
  AntibodyApi,
  AddAntibody,
  CommercialTypeEnum as AntibodyCommercialTypeEnum,
  SearchApi,
  FilterRequest,
  UpdateAntibody
} from "../rest/api";

import { getToken } from "./UserService";

const api = new AntibodyApi();
const searchApi = new SearchApi()

export async function getAntibodies(
  page = 1,
  size = 10
): Promise<PaginatedAntibodies> {
  const abs = (await api.apiRoutersAntibodyGetAntibodies(page, size)).data;
  abs.items = abs.items.map(mapAntibody);
  return abs;
}

function mapAntibody(antibody: Antibody): Antibody {
  if ((!antibody.url) && antibody.vendorUrl) {
    antibody.url = antibody.vendorUrl[0] ?? "-";
  }
  if (antibody.url && !antibody.url.includes("//")) {
    antibody.url = "https://" + antibody.url;
  }

  return antibody;
}


export async function getAntibody(id: number): Promise<Antibody[]> {
  const abs = await (await api.apiRoutersAntibodyGetAntibody(id)).data;
  return abs.map(mapAntibody);
}

export async function addAntibody(antibodyObj: AddAntibody): Promise<any> {
  const ab = mapAntibodyFromForm(antibodyObj);
  return (
    await new AntibodyApi(
      new Configuration({ apiKey: getToken(), accessToken: getToken() })
    ).apiRoutersAntibodyCreateAntibody(ab)
  ).data;
}

function mapAntibodyFromForm(antibody: any): AddAntibody {
  const commercialAb = {
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
    targetSpecies: antibody.targetSpecies.split(/[,;]/).map((app: string) => app.trim()),
    uniprotId: antibody.uniprotID,
    vendorName: antibody.vendor,
    applications: antibody.applications?.split(/[,;]/).map((app: string) => app.trim()),
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
    ).apiRoutersAntibodyGetUserAntibodies(page, size)
  ).data;
}

export async function getSearchAntibodies(
  page = 1,
  size = 10,
  query:string
):Promise<PaginatedAntibodies>{
  const abs = await (
    await searchApi.apiRoutersSearchFtsAntibodies(query, page, size)
  ).data;
  abs.items = abs.items.map(mapAntibody);
  return abs;
}

export async function getFilteredAndSearchedAntibodies(
  filters: FilterRequest = {},
): Promise<PaginatedAntibodies> {
  filters.size = PAGE_SIZE;
  const abs = (
    await searchApi.apiRoutersSearchFilterAntibodies(filters)
  ).data;
  abs.items = abs.items.map(mapAntibody);
  return abs;
}

export async function getAntibodyByAccessionNumber(accesionNumber:number){
  return mapAntibody(await (await api.apiRoutersAntibodyGetByAccession(accesionNumber)).data);
}

export async function updateSubmittedAntibody(updatedAntibody: UpdateAntibody, accesionNumber:number):Promise<Antibody>{
  const ab = mapAntibodyFromForm(updatedAntibody);
  delete ab.vendorName 
  delete ab.catalogNum
  return (
    await new AntibodyApi(
      new Configuration({ apiKey: getToken(), accessToken: getToken() })
    ).apiRoutersAntibodyUpdateUserAntibody(accesionNumber, ab)
  ).data;
}