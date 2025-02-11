import pandas as pd
import json
import os


def load_excel_fast(excel_path, usecols):
    """Loads an Excel file with optimizations, or reads from Parquet if available."""
    parquet_path = excel_path.replace(".xlsx", ".parquet")

    if os.path.exists(parquet_path):  # Load from Parquet if available
        print(f"Loading from Parquet: {parquet_path}")
        df = pd.read_parquet(parquet_path)
    else:  # Convert Excel to Parquet for future fast loads
        print(f"Converting {excel_path} to Parquet for faster access...")
        df = pd.read_excel(excel_path, usecols=usecols, engine="openpyxl")
        df.to_parquet(parquet_path, index=False)

    # Ensure NDC is a string (fix potential integer mismatch issues)
    df["NDC"] = df["NDC"].astype(str)
    return df


def get_tier_counts(ndc_list):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    formulary_xlsx = os.path.join(
        script_dir, "sampled_basic_drugs_formulary_file.xlsx")

    # Load data with optimized dtypes
    formulary_df = load_excel_fast(formulary_xlsx, ['NDC', 'TIER_LEVEL_VALUE'])

    # Ensure TIER_LEVEL_VALUE is an integer and NDC is a string
    formulary_df["NDC"] = formulary_df["NDC"].astype(str)
    formulary_df["TIER_LEVEL_VALUE"] = formulary_df["TIER_LEVEL_VALUE"].astype(
        "int8")

    # Filter for target NDCs
    filtered_df = formulary_df[formulary_df['NDC'].isin(ndc_list)]

    # Count occurrences per tier
    tier_counts = (
        filtered_df.groupby(['NDC', 'TIER_LEVEL_VALUE'])
        .size()
        .unstack(fill_value=0)
        .to_dict(orient='index')
    )

    # Ensure all NDCs appear in output
    result = {}
    for ndc in ndc_list:
        result[ndc] = tier_counts.get(ndc, {})
        # Convert tier keys to strings
        result[ndc] = {str(k): v for k, v in result[ndc].items()}

    return result


def handle_input(input_ndcs):
    cleaned_ndcs = [ndc.strip()
                    for ndc in input_ndcs][:2]  # Ensure exactly 2 NDCs

    # Get tier counts
    counts = get_tier_counts(cleaned_ndcs)

    # Save to JSON
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f"NDC_Tiers_{'_'.join(cleaned_ndcs)}.json"
    )

    with open(output_path, 'w') as f:
        json.dump(counts, f, indent=2)

    print(f"JSON saved to: {output_path}")


if __name__ == "__main__":
    # Get NDC inputs
    input_ndcs = input(
        "Enter two NDCs separated by comma: ").strip().split(',')
    handle_input(input_ndcs)


# import pandas as pd
# import json
# import os


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


# def get_tier_counts(ndc_list):
#     script_dir = os.path.dirname(os.path.abspath(__file__))

#     # Paths for Excel and Parquet files
#     formulary_xlsx = os.path.join(
#         script_dir, "sampled_basic_drugs_formulary_file.xlsx")

#     formulary_parquet = formulary_xlsx.replace(".xlsx", ".parquet")

#     # Load data (only necessary columns)
#     formulary_df = load_excel_fast(
#         formulary_xlsx, ['NDC', 'TIER_LEVEL_VALUE'])

#     # Load formulary data with optimized dtypes
#     # formulary_df = pd.read_excel(
#     #     os.path.join(script_dir, 'sampled_basic_drugs_formulary_file.xlsx'),
#     #     usecols=['NDC', 'TIER_LEVEL_VALUE'],
#     #     dtype={'NDC': 'str', 'TIER_LEVEL_VALUE': 'int8'}
#     # )

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
