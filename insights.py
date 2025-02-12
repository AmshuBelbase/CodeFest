import pandas as pd
import json
import os

# File Paths
file_path = "DSD_PTD_RY24_P04_V10_DY22_BGM.csv"  # Change to your actual file path
parquet_path = file_path.replace(".csv", ".parquet")

# Load from Parquet if available, else convert Excel to Parquet
if os.path.exists(parquet_path):
    print(f"Loading from Parquet: {parquet_path}")
    df = pd.read_parquet(parquet_path)
else:
    print(f"Converting {file_path} to Parquet for faster access...")
    df = pd.read_csv(file_path)
    df.to_parquet(parquet_path, index=False)

# Convert necessary columns to float for proper calculations
df["CAGR_Avg_Spnd_Per_Dsg_Unt_18_22"] = df["CAGR_Avg_Spnd_Per_Dsg_Unt_18_22"].astype(
    float)
df["Chg_Avg_Spnd_Per_Dsg_Unt_21_22"] = df["Chg_Avg_Spnd_Per_Dsg_Unt_21_22"].astype(
    float)

# Yearly data processing
years = list(range(2018, 2023))
year_columns = ["Tot_Spndng_", "Tot_Clms_",
                "Tot_Benes_", "Avg_Spnd_Per_Dsg_Unt_Wghtd_"]

for year in years:
    for col in year_columns:
        col_name = f"{col}{year}"
        if col_name in df.columns:
            df[col_name] = df[col_name].astype(float)

# Directory to store JSON outputs
output_dir = "json_outputs"
os.makedirs(output_dir, exist_ok=True)

# Generate JSON files for different graphs
json_files = {
    "total_spending": {},
    "total_claims": {},
    "total_beneficiaries": {},
    "avg_spending_per_dosage_unit": {},
    "cagr_spending_per_dosage_unit": {},
    "change_spending_per_dosage_unit_21_22": {}
}

for _, row in df.iterrows():
    drug_name = row["Brnd_Name"]

    if drug_name not in json_files["total_spending"]:
        json_files["total_spending"][drug_name] = {}
        json_files["total_claims"][drug_name] = {}
        json_files["total_beneficiaries"][drug_name] = {}
        json_files["avg_spending_per_dosage_unit"][drug_name] = {}

    for year in years:
        json_files["total_spending"][drug_name][year] = row[f"Tot_Spndng_{year}"]
        json_files["total_claims"][drug_name][year] = row[f"Tot_Clms_{year}"]
        json_files["total_beneficiaries"][drug_name][year] = row[f"Tot_Benes_{year}"]
        json_files["avg_spending_per_dosage_unit"][drug_name][
            year] = row[f"Avg_Spnd_Per_Dsg_Unt_Wghtd_{year}"]

    json_files["cagr_spending_per_dosage_unit"][drug_name] = row["CAGR_Avg_Spnd_Per_Dsg_Unt_18_22"]
    json_files["change_spending_per_dosage_unit_21_22"][drug_name] = row["Chg_Avg_Spnd_Per_Dsg_Unt_21_22"]

# Save each category as a separate JSON file
for file_name, data in json_files.items():
    output_json_path = os.path.join(output_dir, f"{file_name}.json")
    with open(output_json_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"JSON saved to: {output_json_path}")
