import os
from functools import reduce

import pandas as pd


def update_vendors(csv_path, vendors_map):
    df_vendor_domain = pd.read_csv(csv_path)
    df_vendor_domain['vendor_id'] = df_vendor_domain['vendor_id'].map(
        lambda x: vendors_map[x] if x in vendors_map else x)
    df_vendor_domain.to_csv(
        f"{os.path.dirname(csv_path)}/{os.path.basename(csv_path).split('.')[0]}_vendors_mapped.csv",
        index=False)


def remove_duplicates(csv_path, cols_subset, chunksize):
    df = reduce(
        lambda df_i, df_j: pd.concat([df_i, df_j])
        .drop_duplicates(subset=cols_subset),
        pd.read_csv(csv_path, chunksize=chunksize)
    )
    df.to_csv(
        f"{os.path.dirname(csv_path)}/{os.path.basename(csv_path).split('.')[0]}_no_duplicates_{'_'.join(cols_subset)}.csv",
        index=False)


if __name__ == '__main__':
    remove_duplicates('../../antibody_table500000.csv', ['ab_id'], 10 ** 4)
    # update_vendors('../../antibody_vendors_domain.csv', {1594: 5187})
    # df_test = pd.read_csv('../../antibody_table500000.csv')
