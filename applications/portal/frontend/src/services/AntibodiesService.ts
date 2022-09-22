import {
  Antibody,
  PaginatedAntibodies,
  AntibodyApi,
  AddUpdateAntibody,
  AntibodyCommercialTypeEnum,
} from "../rest/api";

const api = new AntibodyApi();

export async function getAntibodies(
  page = 0,
  size = 10
): Promise<PaginatedAntibodies> {
  return (await api.getAntibodies(page, size)).data;
}

export async function getAntibody(id: number): Promise<Antibody> {
  return  (await api.getAntibody(id)).data;
}


export async function addAntibody(antibodyObj): Promise<any> {
  let ab = mapAntibody(antibodyObj);
  console.log("mappedObj", ab);
  return (await api.createAntibody(ab)).data;
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
    applications: antibody.applications,
  };
  if (antibody.type === AntibodyCommercialTypeEnum.Commercial) {
    return commercialAb;
  }
  else {
    return { 
      ...commercialAb, 
      definingCitation: antibody.citation
    };}
}
