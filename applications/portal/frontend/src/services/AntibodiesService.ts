import { Configuration } from "../rest";
import {
  Antibody,
  PaginatedAntibodies,
  AntibodyApi,
  AddUpdateAntibody,
  AntibodyCommercialTypeEnum,
  SearchApi
} from "../rest/api";

import { getToken } from "./UserService";

const api = new AntibodyApi();
const searchApi = new SearchApi()

export async function getAntibodies(
  page = 1,
  size = 100
): Promise<PaginatedAntibodies> {
  return (await api.getAntibodies(page, size)).data;
}

export async function getAntibody(id: number): Promise<Antibody[]> {
  return (await api.getAntibody(id)).data;
}

export async function addAntibody(antibodyObj): Promise<any> {
  let ab = mapAntibody(antibodyObj);
  return (
    await new AntibodyApi(
      new Configuration({ apiKey: getToken(), accessToken: getToken() })
    ).createAntibody(ab)
  ).data;
}

function mapAntibody(antibody): AddUpdateAntibody {
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
    targetSpecies: antibody.targetSpecies.split(/\W/),
    uniprotId: antibody.uniprotID,
    vendorName: antibody.vendor,
    applications: antibody.applications.split(/\W/),
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
  size = 100
): Promise<PaginatedAntibodies> {
  return (
    await new AntibodyApi(
      new Configuration({ apiKey: getToken(), accessToken: getToken() })
    ).getUserAntibodies(page, size)
  ).data;
}

export async function getSearchAntibodies(
  page = 1,
  size = 100,
  query:string
):Promise<PaginatedAntibodies>{
  return (
    await searchApi.ftsAntibodies(page, size, query)
  ).data;
}