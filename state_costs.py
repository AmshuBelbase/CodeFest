import pandas as pd
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

# Paths for Excel and Parquet files
beneficiary_xlsx = os.path.join(script_dir, 'sampled_beneficiarycostfile.xlsx')
plan_info_xlsx = os.path.join(script_dir, 'sampled_planinformation.xlsx')

beneficiary_parquet = beneficiary_xlsx.replace(".xlsx", ".parquet")
plan_info_parquet = plan_info_xlsx.replace(".xlsx", ".parquet")


def load_excel_fast(excel_path, usecols):
    """Loads an Excel file with optimizations, or reads from Parquet if available."""
    parquet_path = excel_path.replace(".xlsx", ".parquet")

    if os.path.exists(parquet_path):  # Load from Parquet if it exists
        print(f"Loading from Parquet: {parquet_path}")
        return pd.read_parquet(parquet_path)
    else:  # Convert Excel to Parquet for future fast loads
        print(f"Converting {excel_path} to Parquet for faster access...")
        df = pd.read_excel(excel_path, usecols=usecols, engine="openpyxl")
        df.to_parquet(parquet_path, index=False)
        return df


# Load only required columns
beneficiary_df = load_excel_fast(beneficiary_xlsx, [
    'CONTRACT_ID', 'PLAN_ID', 'SEGMENT_ID',
    'COST_AMT_PREF', 'COST_AMT_NONPREF',
    'COST_AMT_MAIL_PREF', 'COST_AMT_MAIL_NONPREF'
])

plan_info_df = load_excel_fast(plan_info_xlsx, [
    'CONTRACT_ID', 'PLAN_ID', 'SEGMENT_ID', 'STATE'
])

# Merge to link costs with states
merged_df = pd.merge(
    beneficiary_df,
    plan_info_df,
    on=['CONTRACT_ID', 'PLAN_ID', 'SEGMENT_ID'],
    how='left'
)

# Convert cost columns to numeric with reduced memory footprint
cost_columns = [
    'COST_AMT_PREF', 'COST_AMT_NONPREF',
    'COST_AMT_MAIL_PREF', 'COST_AMT_MAIL_NONPREF'
]

merged_df[cost_columns] = merged_df[cost_columns].astype('float32').fillna(0)

# Compute total cost per row
merged_df['total_cost'] = merged_df[cost_columns].sum(axis=1)

# Aggregate by state
state_total = merged_df.groupby('STATE', observed=True)[
    'total_cost'].sum().reset_index()

# Save JSON output
output_json = os.path.join(script_dir, "state_costs.json")
state_total_dict = dict(zip(state_total['STATE'], state_total['total_cost']))

with open(output_json, 'w') as f:
    json.dump(state_total_dict, f, indent=4)

print(f"JSON file '{output_json}' created successfully.")


# import pandas as pd
# import json

# import os

# script_dir = os.path.dirname(os.path.abspath(__file__))

# # Load data from Excel files
# beneficiary_df = pd.read_excel(os.path.join(
#     script_dir, 'sampled_beneficiarycostfile.xlsx'))
# plan_info_df = pd.read_excel(os.path.join(
#     script_dir, 'sampled_planinformation.xlsx'))


# # Merge to link costs with states
# merged_df = pd.merge(
#     beneficiary_df,
#     plan_info_df[['CONTRACT_ID', 'PLAN_ID', 'SEGMENT_ID', 'STATE']],
#     on=['CONTRACT_ID', 'PLAN_ID', 'SEGMENT_ID'],
#     how='left'
# )

# # Define cost columns to sum
# cost_columns = [
#     'COST_AMT_PREF', 'COST_AMT_NONPREF',
#     'COST_AMT_MAIL_PREF', 'COST_AMT_MAIL_NONPREF'
# ]

# # Convert cost columns to numeric and handle missing values
# for col in cost_columns:
#     merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce').fillna(0)

# # Calculate total cost per row
# merged_df['total_cost'] = merged_df[cost_columns].sum(axis=1)

# # Aggregate by state
# state_total = merged_df.groupby('STATE')['total_cost'].sum().reset_index()

# # Create JSON output
# state_total_dict = dict(zip(state_total['STATE'], state_total['total_cost']))
# with open('state_costs.json', 'w') as f:
#     json.dump(state_total_dict, f, indent=4)

# print("JSON file 'state_costs.json' created successfully.")
