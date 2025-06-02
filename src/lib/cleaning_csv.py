import pandas as pd
import glob
import os

source_folder = "../csv"
output_folder = os.path.join(source_folder, "cleaned")
os.makedirs(output_folder, exist_ok=True)

files = glob.glob(os.path.join(source_folder, "MeteoFR_*.csv"))


def cleaned_data(df):
    df = df.dropna(axis=1, how='any')

    df = df.dropna(axis=0, how='all')

    df = df.drop_duplicates()

    df = df.fillna(df.mean(numeric_only=True))

    return df


for f in files:
    our_file = os.path.basename(f)

    df = pd.read_csv(f)
    df_cleaned = cleaned_data(df)

    output = os.path.join(output_folder, f"cleaned_{our_file}")
    df_cleaned.to_csv(output, index=False)
