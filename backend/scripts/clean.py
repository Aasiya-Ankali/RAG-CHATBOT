import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "..","data", "global_power_plant.csv")
output_file_path = os.path.join(BASE_DIR, "..", "data", "cleaned_dataset.csv")

df = pd.read_csv(file_path , low_memory=False)

print(list(df.columns))

def cleaning():
    clean_df = df.copy()
    clean_df.drop_duplicates(inplace=True)
    s = clean_df.shape

    clean_df = clean_df.fillna("")

    col_to_keep = ["country" ,"country_long" ,"name","capacity_mw","latitude","longitude","primary_fuel"]
    clean_df = clean_df[col_to_keep]

    s2 = clean_df.shape
    clean_df.to_csv(output_file_path ,index=False)

    return {
        "shape :" : s,
        "shape after column drop : " : s2,
        "New DF : " : clean_df.to_dict(orient="records") 
    }

print("Cleaned Data is : " ,cleaning())
