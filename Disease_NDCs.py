import pandas as pd
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
print("Load indication data")
# Load indication data
indication_df = pd.read_excel(
    os.path.join(
        script_dir, 'sampled_IndicationBasedCoverageFormularyFile.xlsx'),
    usecols=['RXCUI', 'DISEASE'],
    dtype={'RXCUI': 'str', 'DISEASE': 'str'}
).dropna(subset=['DISEASE'])


def get_ndcs_for_disease(disease_input):

    print("Clean disease name (remove commas and lowercase)")
    # Clean disease name (remove commas and lowercase)
    target_disease = disease_input.strip().replace(',', '').lower()
    indication_df['DISEASE'] = indication_df['DISEASE'].str.lower(
    ).str.replace(',', '')

    print("Get RXCUIs for disease")
    # Get RXCUIs for disease
    rxcuis = indication_df[indication_df['DISEASE']
                           == target_disease]['RXCUI'].unique()

    if not rxcuis.any():
        return {target_disease: []}

    # Load formulary data with memory optimization
    formulary_df = pd.read_excel(
        os.path.join(script_dir, 'sampled_basic_drugs_formulary_file.xlsx'),
        usecols=['RXCUI', 'NDC'],
        dtype={'RXCUI': 'str', 'NDC': 'str'}
    ).dropna(subset=['RXCUI'])

    # Get unique NDCs
    ndc_list = formulary_df[formulary_df['RXCUI'].isin(
        rxcuis)]['NDC'].unique().tolist()

    return {target_disease: sorted(ndc_list)}


if __name__ == "__main__":
    disease = input("Enter disease name: ")
    result = get_ndcs_for_disease(disease)

    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f"{disease.lower().replace(' ', '_').replace(',', '')}_ndcs.json"
    )

    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"JSON saved to: {output_path}")
