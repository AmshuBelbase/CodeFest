import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
insulin_costs = pd.read_csv(
    "insulin beneficiary cost file sample 20250131.txt", sep="|")
plans = pd.read_csv("plan information sample 20250131.txt", sep="|")
drugs = pd.read_csv(
    "basic drugs formulary file sample 20250131.txt", sep="|")

# Convert numeric columns
numeric_cols = ['copay_amt_pref_insln', 'copay_amt_nonpref_insln',
                'copay_amt_mail_pref_insln', 'copay_amt_mail_nonpref_insln']
insulin_costs[numeric_cols] = insulin_costs[numeric_cols].apply(
    pd.to_numeric, errors='coerce')

# --- 1. Insulin Cost Distribution ---
plt.figure(figsize=(10, 5))
sns.boxplot(data=insulin_costs[numeric_cols])
plt.title("Distribution of Insulin Copay Amounts")
plt.xlabel("Copay Type")
plt.ylabel("Amount ($)")
plt.xticks(rotation=15)
plt.show()

# --- 2. Plan Premium & Deductible Analysis ---
plans['PREMIUM'] = pd.to_numeric(plans['PREMIUM'], errors='coerce')
plans['DEDUCTIBLE'] = pd.to_numeric(plans['DEDUCTIBLE'], errors='coerce')

plt.figure(figsize=(10, 5))
sns.histplot(plans['PREMIUM'], bins=20, kde=True)
plt.title("Distribution of Plan Premiums")
plt.xlabel("Premium Amount ($)")
plt.ylabel("Number of Plans")
plt.show()

plt.figure(figsize=(10, 5))
sns.histplot(plans['DEDUCTIBLE'], bins=20, kde=True)
plt.title("Distribution of Plan Deductibles")
plt.xlabel("Deductible Amount ($)")
plt.ylabel("Number of Plans")
plt.show()

# --- 3. Formulary Drug Tier Distribution ---
plt.figure(figsize=(8, 5))
sns.countplot(data=drugs, x='TIER_LEVEL_VALUE',
              order=sorted(drugs['TIER_LEVEL_VALUE'].unique()))
plt.title("Drug Tier Distribution")
plt.xlabel("Tier Level")
plt.ylabel("Number of Drugs")
plt.show()

# --- 4. Geographical Distribution of Plans ---
plt.figure(figsize=(12, 6))
sns.countplot(data=plans, x='STATE', order=plans['STATE'].value_counts().index)
plt.title("Number of Plans by State")
plt.xlabel("State")
plt.ylabel("Number of Plans")
plt.xticks(rotation=45)
plt.show()

print("Visualizations complete!")
