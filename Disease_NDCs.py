import pandas as pd
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
json_filename = "disease_ndcs.json"  # JSON file name

# Paths for Excel and Parquet files
indication_xlsx = os.path.join(
    script_dir, "sampled_IndicationBasedCoverageFormularyFile.xlsx")
formulary_xlsx = os.path.join(
    script_dir, "sampled_basic_drugs_formulary_file.xlsx")

indication_parquet = indication_xlsx.replace(".xlsx", ".parquet")
formulary_parquet = formulary_xlsx.replace(".xlsx", ".parquet")


def load_excel_fast(excel_path, usecols):
    """Loads an Excel file with optimizations, or reads from Parquet if available."""
    parquet_path = excel_path.replace(".xlsx", ".parquet")

    if os.path.exists(parquet_path):  # Load from Parquet if available
        print(f"Loading from Parquet: {parquet_path}")
        return pd.read_parquet(parquet_path)
    else:  # Convert Excel to Parquet for future fast loads
        print(f"Converting {excel_path} to Parquet for faster access...")
        df = pd.read_excel(excel_path, usecols=usecols, engine="openpyxl")
        df.to_parquet(parquet_path, index=False)
        return df


# Load data (only necessary columns)
indication_df = load_excel_fast(
    indication_xlsx, ["RXCUI", "DISEASE"]).dropna(subset=["DISEASE"])
formulary_df = load_excel_fast(
    formulary_xlsx, ["RXCUI", "NDC"]).dropna(subset=["RXCUI"])

# Normalize disease names once (lowercase and remove commas)
indication_df["DISEASE"] = indication_df["DISEASE"].str.lower(
).str.replace(",", "", regex=True)

# Convert `RXCUI` to set for fast lookups
disease_to_rxcui = indication_df.groupby(
    "DISEASE")["RXCUI"].apply(set).to_dict()
rxcui_to_ndc = formulary_df.groupby("RXCUI")["NDC"].apply(set).to_dict()


def get_ndcs_for_disease(disease_input):
    """Fetches NDCs for a given disease."""
    disease_input = disease_input.lower().replace(",", "")

    # Get RXCUIs for the disease
    rxcuis = disease_to_rxcui.get(disease_input, set())
    if not rxcuis:
        return {disease_input: []}

    # Get unique NDCs using set operations for speed
    ndc_list = sorted(
        {ndc for rxcui in rxcuis for ndc in rxcui_to_ndc.get(rxcui, [])})
    return {disease_input: ndc_list}


def update_json_file(disease_name, ndc_list):
    """Updates the JSON file with new NDCs."""
    json_path = os.path.join(script_dir, json_filename)

    # Load existing JSON data if file exists
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    # Update the disease entry
    data[disease_name] = sorted(set(data.get(disease_name, []) + ndc_list))

    # Save updated JSON data
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"JSON updated and saved to: {json_path}")


if __name__ == "__main__":
    while True:
        disease = input("Enter disease name: ").strip(
        ).lower().replace(",", "")
        ndc_result = get_ndcs_for_disease(disease)
        print(ndc_result)

        if ndc_result[disease]:  # Only update if NDCs were found
            update_json_file(disease, ndc_result[disease])
        else:
            print(f"No NDCs found for '{disease}'")


# import pandas as pd
# import json
# import os

# script_dir = os.path.dirname(os.path.abspath(__file__))
# json_filename = "disease_ndcs.json"  # Name of JSON file

# print("Loading indication data...")
# # Load indication data
# indication_df = pd.read_excel(
#     os.path.join(
#         script_dir, "sampled_IndicationBasedCoverageFormularyFile.xlsx"),
#     usecols=["RXCUI", "DISEASE"],
#     dtype={"RXCUI": "str", "DISEASE": "str"},
# ).dropna(subset=["DISEASE"])

# # Load formulary data
# formulary_df = pd.read_excel(
#     os.path.join(script_dir, "sampled_basic_drugs_formulary_file.xlsx"),
#     usecols=["RXCUI", "NDC"],
#     dtype={"RXCUI": "str", "NDC": "str"},
# ).dropna(subset=["RXCUI"])


# def get_ndcs_for_disease(disease_input):
#     global indication_df, script_dir, formulary_df
#     print("Cleaning disease name")

#     # Normalize input disease name
#     target_disease = disease_input
#     indication_df["DISEASE"] = indication_df["DISEASE"].str.lower(
#     ).str.replace(",", "")

#     print("Fetching RXCUIs for disease...")
#     # Get RXCUIs for disease
#     rxcuis = indication_df[indication_df["DISEASE"]
#                            == target_disease]["RXCUI"].unique()

#     if not rxcuis.any():
#         return {target_disease: []}

#     # Get unique NDCs
#     ndc_list = formulary_df[formulary_df["RXCUI"].isin(
#         rxcuis)]["NDC"].unique().tolist()

#     return {target_disease: sorted(ndc_list)}


# def update_json_file(disease_name, ndc_list):
#     json_path = os.path.join(script_dir, json_filename)

#     # Load existing data if JSON file exists
#     if os.path.exists(json_path):
#         with open(json_path, "r", encoding="utf-8") as f:
#             try:
#                 data = json.load(f)
#             except json.JSONDecodeError:
#                 data = {}
#     else:
#         data = {}

#     # Update or add new disease entry
#     data[disease_name] = sorted(set(data.get(disease_name, []) + ndc_list))

#     # Save updated JSON data
#     with open(json_path, "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=2)

#     print(f"JSON updated and saved to: {json_path}")


# if __name__ == "__main__":
#     while True:
#         disease = input("Enter disease name: ").strip()
#         disease = disease.strip().replace(",", "").lower()
#         ndc_result = get_ndcs_for_disease(disease)
#         print(ndc_result)
#         print(disease)
#         if ndc_result[disease]:  # Only update if NDCs were found
#             update_json_file(disease, ndc_result[disease])
#         else:
#             print(f"No NDCs found for '{disease}'")
