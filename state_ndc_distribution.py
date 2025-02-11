import pandas as pd
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

# 1. Load only essential columns with dtype optimization
formulary_cols = ['FORMULARY_ID', 'NDC']
plan_info_cols = ['FORMULARY_ID', 'STATE']

formulary_df = pd.read_excel(
    os.path.join(script_dir, 'sampled_basic_drugs_formulary_file.xlsx'),
    usecols=formulary_cols,
    dtype={'FORMULARY_ID': 'category', 'NDC': 'category'}
)

plan_info_df = pd.read_excel(
    os.path.join(script_dir, 'sampled_planinformation.xlsx'),
    usecols=plan_info_cols,
    dtype={'FORMULARY_ID': 'category', 'STATE': 'category'}
)

# 2. Filter out non-"H" contracts first (where STATE is NaN)
plan_info_df = plan_info_df.dropna(subset=['STATE'])

# 3. Merge using query optimization
merged_df = formulary_df.merge(
    plan_info_df,
    on='FORMULARY_ID',
    how='inner'
)

# 4. Process in chunks for large datasets
chunk_size = 100000
result = {}

for chunk in merged_df.groupby(['NDC', 'STATE']).size().reset_index(name='COUNT').groupby('NDC'):
    ndc = chunk[0]
    states = chunk[1].set_index('STATE')['COUNT'].to_dict()
    result[ndc] = dict(
        sorted(states.items(), key=lambda x: x[1], reverse=True))

# 5. Save to JSON
with open(os.path.join(script_dir, 'state_ndc_distribution.json'), 'w') as f:
    json.dump(result, f, indent=2)

print("JSON file created successfully.")


# import pandas as pd
# import json
# import os

# script_dir = os.path.dirname(os.path.abspath(__file__))

# # Paths for Excel and Parquet files
# formulary_xlsx = os.path.join(
#     script_dir, 'sampled_basic_drugs_formulary_file.xlsx')
# plan_info_xlsx = os.path.join(script_dir, 'sampled_planinformation.xlsx')

# formulary_parquet = formulary_xlsx.replace(".xlsx", ".parquet")
# plan_info_parquet = plan_info_xlsx.replace(".xlsx", ".parquet")


# def load_excel_fast(excel_path, usecols):
#     """Loads an Excel file with optimizations, or reads from Parquet if available."""
#     parquet_path = excel_path.replace(".xlsx", ".parquet")

#     if os.path.exists(parquet_path):  # Load from Parquet if available
#         print(f"Loading from Parquet: {parquet_path}")
#         return pd.read_parquet(parquet_path)
#     else:  # Convert Excel to Parquet for future fast loads
#         print(f"Converting {excel_path} to Parquet for faster access...")
#         df = pd.read_excel(excel_path, usecols=usecols, engine="openpyxl")
#         df.to_parquet(parquet_path, index=False)
#         return df


# # Load optimized data
# formulary_df = load_excel_fast(formulary_xlsx, ['FORMULARY_ID', 'NDC'])
# plan_info_df = load_excel_fast(plan_info_xlsx, ['FORMULARY_ID', 'STATE'])

# # Convert FORMULARY_ID to category (memory efficient)
# formulary_df['FORMULARY_ID'] = formulary_df['FORMULARY_ID'].astype('category')
# plan_info_df['FORMULARY_ID'] = plan_info_df['FORMULARY_ID'].astype('category')

# # Remove duplicate FORMULARY_IDs in plan_info_df to prevent explosion
# plan_info_df = plan_info_df.drop_duplicates(subset=['FORMULARY_ID', 'STATE'])

# # **Check if FORMULARY_ID is causing duplication**
# print(
#     f"Unique FORMULARY_IDs in Formulary: {formulary_df['FORMULARY_ID'].nunique()}")
# print(
#     f"Unique FORMULARY_IDs in Plan Info: {plan_info_df['FORMULARY_ID'].nunique()}")

# # **Safe merge with validation**
# try:
#     merged_df = formulary_df.merge(
#         plan_info_df, on='FORMULARY_ID', how='inner')
# except pd.errors.MergeError as e:
#     print(f"MergeError: {e}")
#     print("Possible reason: FORMULARY_ID is duplicated in both datasets, leading to exponential growth.")
#     exit(1)

# # Group by NDC and STATE
# state_ndc_counts = merged_df.groupby(
#     ['NDC', 'STATE']).size().reset_index(name='COUNT')

# # Convert to dictionary format
# result = state_ndc_counts.pivot(index='NDC', columns='STATE', values='COUNT').fillna(
#     0).astype(int).to_dict(orient='index')

# # Save to JSON
# output_path = os.path.join(script_dir, 'state_ndc_distribution.json')
# with open(output_path, 'w') as f:
#     json.dump(result, f, indent=2)

# print(f"JSON file created successfully: {output_path}")
