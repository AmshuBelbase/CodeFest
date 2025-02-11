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
