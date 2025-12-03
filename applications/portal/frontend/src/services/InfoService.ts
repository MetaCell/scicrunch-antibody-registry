
import {
  GeneralApi as DefaultApi,
  DataInfo,
  PartnerResponseObject,
} from "../rest/api";

const api = new DefaultApi();

export async function getDataInfo():Promise<DataInfo>{
  return (await api.apiRoutersGeneralGetDatainfo()).data;
}

export async function getPartners(): Promise<PartnerResponseObject[]> {
  return (await api.apiRoutersGeneralGetPartners()).data;
}