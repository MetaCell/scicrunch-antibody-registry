import glob
import json
import logging
import os
import time
from typing import List

import pandas as pd
from timeit import default_timer as timer
from api.management.gd_downloader import GDDownloader
from api.models import AntibodyClonality, CommercialType
from areg_portal.settings import RAW_ANTIBODY_DATA, RAW_VENDOR_DATA, RAW_VENDOR_DOMAIN_DATA, CHUNK_SIZE, ANTIBODY_HEADER

MAX_TRIES = 10


class AntibodyMetadata:
    def __init__(self, antibody_data_paths: List[str], vendor_data_path: str, vendor_domain_data_path: str):
        self.antibody_data_paths = antibody_data_paths
        self.vendor_data_path = vendor_data_path
        self.vendor_domain_data_path = vendor_domain_data_path


def clean_df(df):
    df.replace(to_replace=['(null)', '(NaN)'], value=None, inplace=True)


def update_vendors(csv_path: str):
    logging.info("Updating vendors")
    df_vendors = pd.read_csv(csv_path)
    clean_df(df_vendors)
    df_vendors.to_csv(csv_path, index=False, mode='w+')


def update_vendor_domains(csv_path: str, vendors_map_path: str = './vendors_mapping.json'):
    logging.info("Updating vendor domains")
    with open(vendors_map_path, 'r') as f:
        vendors_map = json.load(f)
        df_vendor_domain = pd.read_csv(csv_path)
        df_vendor_domain = df_vendor_domain.drop_duplicates(subset=["domain_name"])
        df_vendor_domain['vendor_id'] = df_vendor_domain['vendor_id'].map(
            lambda x: vendors_map[str(x)] if str(x) in vendors_map else x)
        df_vendor_domain.to_csv(csv_path, index=False, mode='w+')


def replace_file(previous_path, new_path):
    # replace original file with temp file
    os.remove(previous_path)
    tries = 0
    while not os.path.exists(new_path) and tries < MAX_TRIES:
        time.sleep(1)
        tries += 1
    os.rename(new_path, previous_path)


def update_antibodies(csv_paths: List[str], antibodies_map_path: str = './antibodies_mapping.json'):
    logging.info("Updating antibodies")
    with open(antibodies_map_path, 'r') as f:
        antibodies_map = json.load(f)
        for antibody_data_path in csv_paths:
            logging.info(f"Processing {antibody_data_path} file")
            tmp_antibody_data_path = antibody_data_path.replace('.csv', '_tmp.csv')
            for i, chunk in enumerate(pd.read_csv(antibody_data_path, chunksize=CHUNK_SIZE, dtype='unicode')):

                # converge null values to None

                clean_df(chunk)

                # point unknown commercial type and clonality to None and unk

                chunk['commercial_type'].where(chunk['commercial_type'].isin({c[0] for c in CommercialType.choices}),
                                               None, inplace=True)
                chunk['clonality'].where(chunk['clonality'].isin({c[0] for c in AntibodyClonality.choices}), 'unknown',
                                         inplace=True)

                # get rows that need custom update

                relevant_rows = chunk.loc[chunk['ix'].isin(antibodies_map.keys())]

                # apply custom update to relevant rows
                for index, row in relevant_rows.iterrows():
                    for atr in antibodies_map[row['ix']]:
                        chunk.loc[chunk['ix'] == row['ix'], atr] = antibodies_map[row['ix']][atr]

                # save chunk temp file

                chunk.to_csv(tmp_antibody_data_path, mode='a',
                             header=ANTIBODY_HEADER if i == 0 else False, index=False)

            replace_file(antibody_data_path, tmp_antibody_data_path)


def preprocess(file_id: str, dest: str = './antibody_data') -> AntibodyMetadata:
    start = timer()
    logging.info("Preprocessing started")

    gd_downloader = GDDownloader(file_id, dest)
    gd_downloader.download()

    metadata = AntibodyMetadata(glob.glob(os.path.join(dest, '*', f"{RAW_ANTIBODY_DATA}*.csv")),
                                glob.glob(os.path.join(dest, '*', f"{RAW_VENDOR_DATA}.csv"))[0],
                                glob.glob(os.path.join(dest, '*', f"{RAW_VENDOR_DOMAIN_DATA}.csv"))[0])

    update_vendor_domains(metadata.vendor_domain_data_path)
    update_vendors(metadata.vendor_data_path)
    update_antibodies(metadata.antibody_data_paths)

    end = timer()
    logging.info(f"Preprocessing finished in {end - start} seconds")

    return metadata


if __name__ == '__main__':
    preprocess('1gW5fAGRnmm-6zbVRLYJa_zrpEjD4w500')
