import pandas as pd
import json
import os


def get_tier_counts(ndc_list):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(
        script_dir, 'sampled_basic_drugs_formulary_file.xlsx')
    parquet_path = excel_path.replace(".xlsx", ".parquet")

    # Convert Excel to Parquet for speed optimization
    if not os.path.exists(parquet_path):
        print("Converting Excel to Parquet for faster access...")
        df = pd.read_excel(excel_path, usecols=['NDC', 'TIER_LEVEL_VALUE'],
                           dtype={'NDC': 'str'}, engine="openpyxl")
        df['NDC'] = df['NDC'].str.strip()  # Remove extra spaces
        df['TIER_LEVEL_VALUE'] = df['TIER_LEVEL_VALUE'].astype(
            str)  # Convert to string
        df.to_parquet(parquet_path, index=False)
    else:
        print("Loading from Parquet (Much Faster)...")
        df = pd.read_parquet(parquet_path)

    # Filter for target NDCs
    filtered_df = df[df['NDC'].isin(ndc_list)]

    # Count occurrences per tier
    tier_counts = (
        filtered_df.groupby(['TIER_LEVEL_VALUE', 'NDC'])
        .size()
        .unstack(fill_value=0)
        .reset_index()
        .rename(columns={'TIER_LEVEL_VALUE': 'name'})
        .to_dict(orient='records')
    )

    # Ensure all NDCs appear in each tier entry
    for entry in tier_counts:
        entry['name'] = str(entry['name'])  # Convert name to string
        for ndc in ndc_list:
            # Ensure NDC exists in output with 0 if missing
            entry.setdefault(ndc, 0)

    return tier_counts


if __name__ == "__main__":
    input_ndcs = input(
        "Enter two NDCs separated by comma: ").strip().split(',')
    cleaned_ndcs = [ndc.strip()
                    for ndc in input_ndcs][:2]  # Ensure exactly 2 NDCs

    counts = get_tier_counts(cleaned_ndcs)

    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f"NDC_Tiers_{'_'.join(cleaned_ndcs)}.json"
    )

    with open(output_path, 'w') as f:
        json.dump(counts, f, indent=2)

    print(f"JSON saved to: {output_path}")


# import pandas as pd
# import json
# import os


# def get_tier_counts(ndc_list):
#     script_dir = os.path.dirname(os.path.abspath(__file__))

#     # Load formulary data with optimized dtypes
#     formulary_df = pd.read_excel(
#         os.path.join(script_dir, 'sampled_basic_drugs_formulary_file.xlsx'),
#         usecols=['NDC', 'TIER_LEVEL_VALUE'],
#         dtype={'NDC': 'str', 'TIER_LEVEL_VALUE': 'int8'}
#     )

#     # Filter for target NDCs
#     filtered_df = formulary_df[formulary_df['NDC'].isin(ndc_list)]

#     # Count occurrences per tier
#     tier_counts = (
#         filtered_df.groupby(['NDC', 'TIER_LEVEL_VALUE'])
#         .size()
#         .unstack(fill_value=0)
#         .to_dict(orient='index')
#     )

#     # Ensure all NDCs appear in output
#     result = {}
#     for ndc in ndc_list:
#         result[ndc] = tier_counts.get(ndc, {})
#         # Convert tier numbers to strings for JSON compatibility
#         result[ndc] = {str(k): v for k, v in result[ndc].items()}

#     return result


# if __name__ == "__main__":
#     # Get NDC inputs
#     input_ndcs = input(
#         "Enter two NDCs separated by comma: ").strip().split(',')
#     cleaned_ndcs = [ndc.strip()
#                     for ndc in input_ndcs][:2]  # Ensure exactly 2 NDCs

#     # Get tier counts
#     counts = get_tier_counts(cleaned_ndcs)

#     # Save to JSON
#     output_path = os.path.join(
#         os.path.dirname(os.path.abspath(__file__)),
#         f"NDC_Tiers_{'_'.join(cleaned_ndcs)}.json"
#     )

#     with open(output_path, 'w') as f:
#         json.dump(counts, f, indent=2)

#     print(f"JSON saved to: {output_path}")
