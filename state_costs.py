import pandas as pd
import json

import os

script_dir = os.path.dirname(os.path.abspath(__file__))

print("1")
# Load data from Excel files
beneficiary_df = pd.read_excel(os.path.join(
    script_dir, 'sampled_beneficiarycostfile.xlsx'))
print("2")
plan_info_df = pd.read_excel(os.path.join(
    script_dir, 'sampled_planinformation.xlsx'))
print("3")


# Merge to link costs with states
merged_df = pd.merge(
    beneficiary_df,
    plan_info_df[['CONTRACT_ID', 'PLAN_ID', 'SEGMENT_ID', 'STATE']],
    on=['CONTRACT_ID', 'PLAN_ID', 'SEGMENT_ID'],
    how='left'
)

# Define cost columns to sum
cost_columns = [
    'COST_AMT_PREF', 'COST_AMT_NONPREF',
    'COST_AMT_MAIL_PREF', 'COST_AMT_MAIL_NONPREF'
]

# Convert cost columns to numeric and handle missing values
for col in cost_columns:
    merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce').fillna(0)

# Calculate total cost per row
merged_df['total_cost'] = merged_df[cost_columns].sum(axis=1)

# Aggregate by state
state_total = merged_df.groupby('STATE')['total_cost'].sum().reset_index()

# Create JSON output
state_total_dict = dict(zip(state_total['STATE'], state_total['total_cost']))
with open('state_costs.json', 'w') as f:
    json.dump(state_total_dict, f, indent=4)

print("JSON file 'state_costs.json' created successfully.")
