import pandas as pd
from glob import glob

base_directory = "/mnt/c/Users/filip/Downloads/antibodyregistry_shared"


def xlsx_to_csv(filename):
    df = pd.read_excel(filename)
    df.to_csv(filename.replace(".xlsx", ".csv"), index=False)


for filename in glob(base_directory + "/*.xlsx"):
    xlsx_to_csv(filename)
