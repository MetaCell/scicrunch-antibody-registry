import glob
import json
import logging
import os
from typing import List

import pandas as pd
from timeit import default_timer as timer
from api.management.gd_downloader import GDDownloader
from areg_portal.settings import RAW_ANTIBODY_DATA, RAW_VENDOR_DATA, RAW_VENDOR_DOMAIN_DATA, CHUNK_SIZE, ANTIBODY_HEADER


class AntibodyMetadata:
    def __init__(self, antibody_data_paths: List[str], vendor_data_path: str, vendor_domain_data_path: str):
        self.antibody_data_paths = antibody_data_paths
        self.vendor_data_path = vendor_data_path
        self.vendor_domain_data_path = vendor_domain_data_path


def update_vendors(csv_path: str, vendors_map_path: str = './vendors_mapping.json'):
    logging.info("Updating vendors")
    with open(vendors_map_path, 'r') as f:
        vendors_map = json.load(f)
        df_vendor_domain = pd.read_csv(csv_path)
        df_vendor_domain['vendor_id'] = df_vendor_domain['vendor_id'].map(
            lambda x: vendors_map[str(x)] if str(x) in vendors_map else x)
        df_vendor_domain.to_csv(csv_path, index=False, mode='w+')


def update_antibodies(csv_paths: List[str], antibodies_map_path: str = './antibodies_mapping.json'):
    logging.info("Updating antibodies")
    with open(antibodies_map_path, 'r') as f:
        antibodies_map = json.load(f)
        for antibody_data_path in csv_paths:
            tmp_antibody_data_path = antibody_data_path.replace('.csv', '_tmp.csv')
            for i, chunk in enumerate(pd.read_csv(antibody_data_path, chunksize=CHUNK_SIZE, dtype='unicode')):
                relevant_rows = chunk.loc[chunk['ab_id'].isin(antibodies_map.keys())]
                for index, row in relevant_rows.iterrows():
                    for atr in antibodies_map[row['ab_id']]:
                        row['atr'] = antibodies_map[row['ab_id']][atr]
                chunk.to_csv(tmp_antibody_data_path, mode='a',
                             header=ANTIBODY_HEADER if i == 0 else False, index=False)
            os.remove(antibody_data_path)
            os.rename(tmp_antibody_data_path, antibody_data_path)


def preprocess(file_id: str, dest: str = './antibody_data') -> AntibodyMetadata:
    start = timer()
    logging.info("Preprocessing started")
    gd_downloader = GDDownloader(file_id, dest)
    gd_downloader.download()
    metadata = AntibodyMetadata(glob.glob(os.path.join(dest, '*', f"{RAW_ANTIBODY_DATA}*.csv")),
                                glob.glob(os.path.join(dest, '*', f"{RAW_VENDOR_DATA}.csv"))[0],
                                glob.glob(os.path.join(dest, '*', f"{RAW_VENDOR_DOMAIN_DATA}.csv"))[0])
    update_vendors(metadata.vendor_domain_data_path)
    update_antibodies(metadata.antibody_data_paths)
    end = timer()
    logging.info(f"Preprocessing finished in {end - start} seconds")
    return metadata


if __name__ == '__main__':
    preprocess('1gW5fAGRnmm-6zbVRLYJa_zrpEjD4w500')
