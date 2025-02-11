import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

folder_path = os.path.dirname(os.path.abspath(__file__))
print(folder_path)

# Configuration
pd.set_option('display.max_columns', None)
plt.style.use('ggplot')

# Load data with proper error handling


def load_data(file_path, columns=None):
    try:
        # Try reading normally first
        return pd.read_csv(file_path, dtype='str', low_memory=False)
    except pd.errors.ParserError:
        # If structure issues exist, skip bad lines
        return pd.read_csv(file_path, dtype='str', on_bad_lines='skip')


# Load all datasets
formulary = load_data(os.path.join(
    folder_path, 'sampled_basic_drugs_formulary_file.csv'))
beneficiary_cost = load_data(os.path.join(
    folder_path, 'sampled_beneficiarycostfile.csv'))
excluded_drugs = load_data(os.path.join(
    folder_path, 'sampled_excludeddrugsfomularyfile.csv'))
geographic = load_data(os.path.join(
    folder_path, 'sampled_geographiclocatorfile.csv'))


pharmacy_networks = pd.concat([load_data(os.path.join(
    folder_path, f'sampled_pharmacynetworks{i}.csv'))
    for i in range(1, 7)])

plan_info = load_data(os.path.join(
    folder_path, 'sampled_planinformation.csv'))

# Assume company drug identifiers (replace with actual NDCs/RXCUIs)
# Example NDCs from formulary sample
company_drugs = ['2145780', '2149580', '2237711']

# Tier Analysis


def analyze_tiers(company_drug):
    # Filter company drugs
    global formulary
    company_drugs = [company_drug]
    company_data = formulary[formulary['NDC'].isin(company_drugs)]

    # Get distributions
    tier_dist = formulary['TIER_LEVEL_VALUE'].value_counts().sort_index()
    company_tier_dist = company_data['TIER_LEVEL_VALUE'].value_counts(
    ).sort_index()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    ax1.bar(tier_dist.index, tier_dist.values,
            color='lightblue', label='All Drugs')
    ax2.bar(company_tier_dist.index, company_tier_dist.values,
            color='darkred', label='Company Drugs')

    # plt.xlabel('Tier Level')
    ax1.set_xlabel('Tier Level')
    ax2.set_xlabel('Tier Level')

    ax1.set_ylabel('Count of Drugs')
    ax2.set_ylabel('Count of Drugs')

    # plt.ylabel('Count of Drugs')
    plt.legend()
    plt.show()

    return company_data

# Cost Sharing Analysis


def analyze_costs(company_data, beneficiary_cost):
    print("Company Data Columns:", company_data.columns)
    print("Beneficiary Cost Columns:", beneficiary_cost.columns)

    merged = pd.merge(company_data, beneficiary_cost,
                      on=['CONTRACT_ID', 'PLAN_ID'], how='left')

    # Clean cost columns
    cost_cols = ['COST_AMT_PREF', 'COST_AMT_NONPREF', 'COST_AMT_MAIL_PREF']
    for col in cost_cols:
        merged[col] = pd.to_numeric(merged[col], errors='coerce')

    # Aggregate costs
    cost_analysis = merged.groupby('TIER_LEVEL_VALUE')[cost_cols].mean()

    # Plot
    plt.figure(figsize=(12, 6))
    cost_analysis.plot(kind='bar')
    plt.title('Average Cost Sharing by Tier Level')
    plt.ylabel('Cost Amount ($)')
    plt.xlabel('Tier Level')
    plt.xticks(rotation=0)
    plt.show()

    return cost_analysis

# Restrictions Analysis


def analyze_restrictions(company_data):
    restrictions = company_data[['PRIOR_AUTHORIZATION_YN', 'STEP_THERAPY_YN',
                                'QUANTITY_LIMIT_YN']].apply(pd.Series.value_counts)

    plt.figure(figsize=(8, 4))
    restrictions.T.plot(kind='bar', stacked=True)
    plt.title('Restrictions on Company Drugs')
    plt.ylabel('Count of Drugs')
    plt.show()

    return restrictions

# Pharmacy Network Coverage


def analyze_pharmacy_coverage(pharmacy_networks, plan_info):
    # Merge with plan info
    merged = pd.merge(pharmacy_networks, plan_info,
                      on=['CONTRACT_ID', 'PLAN_ID'], how='left')

    # Calculate preferred pharmacy coverage
    pref_coverage = merged.groupby('CONTRACT_ID')[
        'PREFERRED_STATUS_RETAIL'].value_counts(normalize=True)

    plt.figure(figsize=(10, 6))
    pref_coverage.unstack().plot(kind='bar', stacked=True)
    plt.title('Preferred Pharmacy Coverage by Contract')
    plt.ylabel('Proportion of Pharmacies')
    plt.show()

    return pref_coverage


# Main Analysis
print("Analyzing Tier Distribution...")
company_drug_data = analyze_tiers(company_drugs[0])

print("\nAnalyzing Cost Sharing...")
cost_analysis = analyze_costs(company_drug_data, beneficiary_cost)

print("\nAnalyzing Restrictions...")
restrictions = analyze_restrictions(company_drug_data)

print("\nAnalyzing Pharmacy Network Coverage...")
pharmacy_coverage = analyze_pharmacy_coverage(pharmacy_networks, plan_info)

# Generate Recommendations


def generate_recommendations(company_drug_data, cost_analysis):
    recommendations = []

    # Tier optimization
    current_tiers = company_drug_data['TIER_LEVEL_VALUE'].unique()
    optimal_tiers = cost_analysis.idxmin(axis=1)

    for drug in company_drug_data['NDC'].unique():
        current_tier = company_drug_data[company_drug_data['NDC'] == drug]['TIER_LEVEL_VALUE'].mode()[
            0]
        recommended_tier = optimal_tiers.get(current_tier, current_tier)

        recommendations.append({
            'NDC': drug,
            'Current Tier': current_tier,
            'Recommended Tier': recommended_tier,
            'Potential Cost Reduction (%)': (
                (cost_analysis.loc[current_tier].mean() -
                 cost_analysis.loc[recommended_tier].mean()) /
                cost_analysis.loc[current_tier].mean()) * 100
        })

    return pd.DataFrame(recommendations)


print("\nGenerating Recommendations...")
recommendations = generate_recommendations(company_drug_data, cost_analysis)
print("\nTop Recommendations:")
print(recommendations.sort_values(
    'Potential Cost Reduction (%)', ascending=False))
