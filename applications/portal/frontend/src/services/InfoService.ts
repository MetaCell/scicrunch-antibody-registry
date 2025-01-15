
import {
  DefaultApi,
  DataInfo,
  PartnerResponseObject,
} from "../rest/api";

const api = new DefaultApi();

export async function getDataInfo():Promise<DataInfo>{
  return (await api.datainfoGet()).data;
}

export async function getPartners(): Promise<PartnerResponseObject[]> {
  return (await api.getPartners()).data;
}