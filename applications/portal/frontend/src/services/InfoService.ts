
import {
  DefaultApi,
  DataInfo,
} from "../rest/api";

const api = new DefaultApi();

export async function getDataInfo():Promise<DataInfo>{
  return (await api.datainfoGet()).data;
}