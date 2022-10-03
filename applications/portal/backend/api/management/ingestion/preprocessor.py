import glob
import json
import logging
import os
from typing import List

import pandas as pd

from api.management.ingestion.gd_downloader import GDDownloader
from api.models import AntibodyClonality, CommercialType
from api.services.filesystem_service import replace_file
from api.utilities.decorators import timed_class_method
from areg_portal.settings import RAW_ANTIBODY_DATA_BASENAME, RAW_VENDOR_DATA_BASENAME, RAW_VENDOR_DOMAIN_DATA_BASENAME, \
    CHUNK_SIZE, \
    ANTIBODY_HEADER, RAW_USERS_DATA_BASENAME, DEFAULT_UID

UNKNOWN_VENDORS = {'1669', '1667', '1625', '1633', '1628', '11599', '12068', '12021', '1632', '5455', '1626', '1670',
                   '11278', '(null)', '1684', '11598', '0', '1682', '11434'}

UNKNOWN_USERS = {'3483', '1473', '3208', '3519', '21828', '30083', '7650', '7574', '27908', '3169', '3711', '5627',
                 '37877', '37922', '669', '30887', '3336', '8293', '1176', '7948', '37896', '8521', '37900', '9540',
                 '2209', '3082', '31464', '32106', '1282', '3671', '9132', '2892', '22915', '5047', '1175', '1883',
                 '31166', '8612', '8016', '7706'}


class AntibodyMetadata:
    def __init__(self, antibody_data_paths: List[str], vendor_data_path: str, vendor_domain_data_path: str,
                 users_data_path: str):
        self.antibody_data_paths = antibody_data_paths
        self.vendor_data_path = vendor_data_path
        self.vendor_domain_data_path = vendor_domain_data_path
        self.users_data_path = users_data_path


def clean_df(df):
    df.replace(to_replace=['(null)', '(NaN)'], value=None, inplace=True)


def update_vendors(csv_path: str):
    logging.info("Updating vendors")
    df_vendors = pd.read_csv(csv_path)
    clean_df(df_vendors)
    df_vendors.to_csv(csv_path, index=False, mode='w+')


def update_users(csv_path: str):
    logging.info("Updating users")
    df_users = pd.read_csv(csv_path)
    # df_users = df_users.drop(['password', 'salt'], axis=1)
    df_users = df_users.drop_duplicates(['email'], keep='last').loc[~df_users['email'].isnull()]
    df_users = df_users.loc[df_users['banned'] != 1]
    df_users = df_users.loc[~df_users['guid'].isnull()]
    clean_df(df_users)
    df_users.to_csv(csv_path, index=False, mode='w+')


def update_vendor_domains(csv_path: str, vendors_map_path: str = './vendors_mapping.json'):
    logging.info("Updating vendor domains")
    with open(vendors_map_path, 'r') as f:
        vendors_map = json.load(f)
        df_vendor_domain = pd.read_csv(csv_path)
        df_vendor_domain = df_vendor_domain.drop_duplicates(subset=["domain_name"])
        df_vendor_domain['vendor_id'] = df_vendor_domain['vendor_id'].map(
            lambda x: vendors_map[str(x)] if str(x) in vendors_map else x)
        df_vendor_domain.to_csv(csv_path, index=False, mode='w+')


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

                # lowercase necessary columns
                chunk["source_organism"] = chunk["source_organism"].str.lower()
                chunk["link"] = chunk["link"].str.lower()

                # point unknown vendor_id to None
                chunk['vendor_id'] = chunk['vendor_id'].where(~chunk['vendor_id'].isin(UNKNOWN_VENDORS), None)

                # point unknown user_id to None
                chunk['uid'] = chunk['uid'].where(~chunk['uid'].isin(UNKNOWN_USERS), DEFAULT_UID)

                # point unknown commercial type to None
                chunk['commercial_type'] = chunk['commercial_type'].where(
                    chunk['commercial_type'].isin({c[0] for c in CommercialType.choices}),
                    None)

                # point unknown clonality to 'unknown'
                chunk['clonality'] = chunk['clonality'].where(
                    chunk['clonality'].isin({c[0] for c in AntibodyClonality.choices}), 'unknown')

                # get rows that need custom update
                relevant_rows = chunk.loc[chunk['ix'].isin(antibodies_map.keys())]

                # apply custom update to relevant rows
                for index, row in relevant_rows.iterrows():
                    for atr in antibodies_map[row['ix']]:
                        chunk.loc[chunk['ix'] == row['ix'], atr] = antibodies_map[row['ix']][atr]

                # save chunk temp file
                chunk.to_csv(tmp_antibody_data_path, mode='a',
                             header=ANTIBODY_HEADER.keys() if i == 0 else False, index=False)

            replace_file(antibody_data_path, tmp_antibody_data_path)


class Preprocessor:
    def __init__(self, file_id: str, dest: str = './antibody_data'):
        self.file_id = file_id
        self.dest = dest

    @timed_class_method('Preprocessing finished')
    def preprocess(self) -> AntibodyMetadata:
        logging.info("Preprocessing started")

        GDDownloader(self.file_id, self.dest).download()

        metadata = AntibodyMetadata(glob.glob(os.path.join(self.dest, '*', f"{RAW_ANTIBODY_DATA_BASENAME}*.csv")),
                                    glob.glob(os.path.join(self.dest, '*', f"{RAW_VENDOR_DATA_BASENAME}.csv"))[0],
                                    glob.glob(os.path.join(self.dest, '*', f"{RAW_VENDOR_DOMAIN_DATA_BASENAME}.csv"))[
                                        0],
                                    glob.glob(os.path.join(self.dest, '*', f"{RAW_USERS_DATA_BASENAME}.csv"))[0])

        # update_vendor_domains(metadata.vendor_domain_data_path)
        # update_vendors(metadata.vendor_data_path)
        # update_antibodies(metadata.antibody_data_paths)
        # update_users(metadata.users_data_path)

        return metadata
