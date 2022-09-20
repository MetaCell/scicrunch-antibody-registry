import glob
import json
import os

import pandas as pd

from api.management.gd_downloader import GDDownloader
from areg_portal.settings import RAW_ANTIBODY_DATA, RAW_VENDOR_DATA, RAW_VENDOR_DOMAIN_DATA


class AntibodyMetadata:
    def __init__(self, antibody_data_path: str, vendor_data_path: str, vendor_domain_data_path: str):
        self.antibody_data_path = antibody_data_path
        self.vendor_data_path = vendor_data_path
        self.vendor_domain_data_path = vendor_domain_data_path


def update_vendors(csv_path: str, vendors_map_path: str = './vendors_mapping.json'):
    with open(vendors_map_path, 'r') as f:
        vendors_map = json.load(f)
        df_vendor_domain = pd.read_csv(csv_path)
        df_vendor_domain['vendor_id'] = df_vendor_domain['vendor_id'].map(
            lambda x: vendors_map[str(x)] if str(x) in vendors_map else x)
        df_vendor_domain.to_csv(csv_path, index=False, mode='w+')


def preprocess(file_id: str, dest: str = './antibody_data') -> AntibodyMetadata:
    gd_downloader = GDDownloader(file_id, dest)
    gd_downloader.download()
    metadata = AntibodyMetadata(glob.glob(os.path.join(dest, '*', RAW_ANTIBODY_DATA))[0],
                                glob.glob(os.path.join(dest, '*', RAW_VENDOR_DATA))[0],
                                glob.glob(os.path.join(dest, '*', RAW_VENDOR_DOMAIN_DATA))[0])
    update_vendors(metadata.vendor_domain_data_path)
    return metadata


if __name__ == '__main__':
    preprocess('1gW5fAGRnmm-6zbVRLYJa_zrpEjD4w500')
