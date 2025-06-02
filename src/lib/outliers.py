import os
import pandas as pd
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))
cleaned_folder = os.path.join(current_dir, "..", "csv", "cleaned")
cleaned_folder = os.path.normpath(cleaned_folder)


def replace_outliers_with_mean(df, threshold=1.5):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        is_outlier = (df[col] < lower_bound) | (df[col] > upper_bound)
        mean_value = df[col][~is_outlier].mean()
        df.loc[is_outlier, col] = mean_value
    return df


for filename in os.listdir(cleaned_folder):
    if filename.startswith("cleaned_MeteoFR_") and filename.endswith(".csv"):
        file_path = os.path.join(cleaned_folder, filename)
        print(f"📄 Traitement du fichier : {filename}")

        df = pd.read_csv(file_path)

        df_cleaned = replace_outliers_with_mean(df)

        df_cleaned.to_csv(file_path, index=False)
        print(f"✅ Fichier mis à jour : {filename}")
