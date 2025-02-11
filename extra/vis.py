import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load data (replace file paths with actual paths)
basic_formulary = pd.read_csv(
    r"MonthlyPrescriptionDrugPlanFormularyandPharmacyNetworkInformation\2025-01\2025_20250123\basic_drugs_formulary_file.txt", delimiter="|")
beneficiary_cost = pd.read_csv(
    r"MonthlyPrescriptionDrugPlanFormularyandPharmacyNetworkInformation\2025-01\2025_20250123\beneficiarycostfile.txt", delimiter="|")
excluded_drugs = pd.read_csv(
    r"MonthlyPrescriptionDrugPlanFormularyandPharmacyNetworkInformation\2025-01\2025_20250123\excludeddrugsfomularyfile.txt", delimiter="|")
geographic_locator = pd.read_csv(
    r"MonthlyPrescriptionDrugPlanFormularyandPharmacyNetworkInformation\2025-01\2025_20250123\geographiclocatorfile.txt", delimiter="|")
indication_coverage = pd.read_csv(
    r"MonthlyPrescriptionDrugPlanFormularyandPharmacyNetworkInformation\2025-01\2025_20250123\IndicationBasedCoverageFormularyFile.txt", delimiter="|")
insulin_cost = pd.read_csv(
    r"MonthlyPrescriptionDrugPlanFormularyandPharmacyNetworkInformation\2025-01\2025_20250123\insulinbeneficiarycostfile.txt", delimiter="|")
pharmacy_networks = pd.concat([pd.read_csv(
    rf"MonthlyPrescriptionDrugPlanFormularyandPharmacyNetworkInformation\2025-01\2025_20250123\pharmacynetworks{i}.txt", delimiter="|") for i in range(1, 7)])
plan_info = pd.read_csv(
    r"MonthlyPrescriptionDrugPlanFormularyandPharmacyNetworkInformation\2025-01\2025_20250123\planinformation.txt", delimiter="|")

# 1. Formulary Tier Distribution
plt.figure(figsize=(10, 6))
sns.countplot(data=basic_formulary, x="TIER_LEVEL_VALUE")
plt.title("Formulary Tier Distribution")
plt.xlabel("Tier Level")
plt.ylabel("Number of Drugs")
plt.show()

# 2. Cost-Sharing Comparison (Preferred vs. Non-Preferred)
plt.figure(figsize=(10, 6))
sns.barplot(data=beneficiary_cost, x="RXCUI",
            y="COST_AMT_PREF", color="blue", label="Preferred")
sns.barplot(data=beneficiary_cost, x="RXCUI", y="COST_AMT_NONPREF",
            color="red", label="Non-Preferred")
plt.title("Cost-Sharing Comparison")
plt.xlabel("Drug RXCUI")
plt.ylabel("Cost Amount")
plt.legend()
plt.show()

# 3. Quantity Limits and Restrictions
restrictions = basic_formulary[[
    "QUANTITY_LIMIT_YN", "PRIOR_AUTHORIZATION_YN", "STEP_THERAPY_YN"]].sum().reset_index()
restrictions.columns = ["Restriction", "Count"]
plt.figure(figsize=(10, 6))
sns.barplot(data=restrictions, x="Restriction", y="Count")
plt.title("Quantity Limits and Restrictions")
plt.xlabel("Restriction Type")
plt.ylabel("Count")
plt.show()

# 4. Geographic Coverage by Region
region_coverage = plan_info.groupby(
    "MA_REGION_CODE").size().reset_index(name="Count")
fig = px.choropleth(region_coverage, locations="MA_REGION_CODE",
                    locationmode="USA-states", color="Count", scope="usa")
fig.update_layout(title="Geographic Coverage by Region")
fig.show()

# 5. Insulin Copay Comparison
plt.figure(figsize=(10, 6))
sns.lineplot(data=insulin_cost, x="DAYS_SUPPLY",
             y="copay_amt_pref_insln", label="Preferred")
sns.lineplot(data=insulin_cost, x="DAYS_SUPPLY",
             y="copay_amt_nonpref_insln", label="Non-Preferred")
plt.title("Insulin Copay Comparison")
plt.xlabel("Days Supply")
plt.ylabel("Copay Amount")
plt.legend()
plt.show()

# 6. Pharmacy Network Dispensing Fees
plt.figure(figsize=(10, 6))
sns.boxplot(data=pharmacy_networks, x="PREFERRED_STATUS_RETAIL",
            y="BRAND_DISPENSING_FEE_30")
plt.title("Pharmacy Network Dispensing Fees")
plt.xlabel("Preferred Status")
plt.ylabel("Dispensing Fee")
plt.show()

# 7. Plan Premiums and Deductibles
plt.figure(figsize=(10, 6))
sns.scatterplot(data=plan_info, x="PREMIUM", y="DEDUCTIBLE")
plt.title("Plan Premiums vs. Deductibles")
plt.xlabel("Premium")
plt.ylabel("Deductible")
plt.show()

# 8. Excluded Drugs by Plan
excluded_counts = excluded_drugs.groupby(["PLAN_ID", "RXCUI"]).size().unstack()
plt.figure(figsize=(12, 8))
sns.heatmap(excluded_counts, cmap="YlOrRd")
plt.title("Excluded Drugs by Plan")
plt.xlabel("Drug RXCUI")
plt.ylabel("Plan ID")
plt.show()

# 9. Indication-Based Coverage
disease_counts = indication_coverage.groupby(
    "DISEASE").size().reset_index(name="Count")
fig = px.treemap(disease_counts, path=["DISEASE"], values="Count")
fig.update_layout(title="Indication-Based Coverage")
fig.show()

# 10. Preferred vs. Non-Preferred Pharmacy Distribution
preferred_counts = pharmacy_networks["PREFERRED_STATUS_RETAIL"].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(preferred_counts, labels=preferred_counts.index, autopct="%1.1f%%")
plt.title("Preferred vs. Non-Preferred Pharmacy Distribution")
plt.show()

# 11. Cost-Sharing by Tier
plt.figure(figsize=(10, 6))
sns.barplot(data=beneficiary_cost, x="TIER",
            y="COST_AMT_PREF", label="Preferred")
sns.barplot(data=beneficiary_cost, x="TIER",
            y="COST_AMT_NONPREF", label="Non-Preferred")
plt.title("Cost-Sharing by Tier")
plt.xlabel("Tier")
plt.ylabel("Cost Amount")
plt.legend()
plt.show()

# 12. Mail-Order vs. Retail Cost Comparison
plt.figure(figsize=(10, 6))
sns.lineplot(data=beneficiary_cost, x="DAYS_SUPPLY",
             y="COST_AMT_MAIL_PREF", label="Mail-Order Preferred")
sns.lineplot(data=beneficiary_cost, x="DAYS_SUPPLY",
             y="COST_AMT_PREF", label="Retail Preferred")
plt.title("Mail-Order vs. Retail Cost Comparison")
plt.xlabel("Days Supply")
plt.ylabel("Cost Amount")
plt.legend()
plt.show()

# 13. Plan Suppression Analysis
suppressed_counts = plan_info["PLAN_SUPPRESSED_YN"].value_counts()
plt.figure(figsize=(8, 6))
sns.barplot(x=suppressed_counts.index, y=suppressed_counts.values)
plt.title("Plan Suppression Analysis")
plt.xlabel("Plan Suppressed (Y/N)")
plt.ylabel("Count")
plt.show()

# 14. Specialty Tier Analysis
plt.figure(figsize=(10, 6))
sns.countplot(data=beneficiary_cost, x="TIER", hue="TIER_SPECIALTY_YN")
plt.title("Specialty Tier Analysis")
plt.xlabel("Tier")
plt.ylabel("Count")
plt.legend(title="Specialty Tier")
plt.show()

# 15. Copay Distribution for Insulin
plt.figure(figsize=(10, 6))
sns.histplot(data=insulin_cost, x="copay_amt_pref_insln", bins=20, kde=True)
plt.title("Copay Distribution for Insulin")
plt.xlabel("Copay Amount")
plt.ylabel("Frequency")
plt.show()
