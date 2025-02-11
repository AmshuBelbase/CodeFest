import streamlit as st
import plotly.express as px
from pyspark.sql import SparkSession
import os
from pyspark.sql.functions import col

# Initialize Spark session
spark = SparkSession.builder.appName("PharmaceuticalAnalysis").getOrCreate()

# Get file path
fp = os.path.dirname(os.path.abspath(__file__))

fn = "basic_drugs_formulary_file.txt"
file_path = os.path.join(fp, fn)
basic_formulary_df = spark.read.csv(
    file_path, sep="|", header=True, inferSchema=True)

fn = "beneficiarycostfile.txt"
file_path = os.path.join(fp, fn)
beneficiary_cost_df = spark.read.csv(
    file_path, sep="|", header=True, inferSchema=True)


fn = "excludeddrugsfomularyfile.txt"
file_path = os.path.join(fp, fn)
excluded_drugs_df = spark.read.csv(
    file_path, sep="|", header=True, inferSchema=True)

fn = "geographiclocatorfile.txt"
file_path = os.path.join(fp, fn)
geographic_locator_df = spark.read.csv(
    file_path, sep="|", header=True, inferSchema=True)


fn = "IndicationBasedCoverageFormularyFile.txt"
file_path = os.path.join(fp, fn)
indication_coverage_df = spark.read.csv(
    file_path, sep="|", header=True, inferSchema=True)

fn = "insulinbeneficiarycostfile.txt"
file_path = os.path.join(fp, fn)
insulin_cost_df = spark.read.csv(
    file_path, sep="|", header=True, inferSchema=True)

fn = "pharmacynetworks1.txt"
file_path = os.path.join(fp, fn)
pharmacy_networks_df = spark.read.csv(
    file_path, sep="|", header=True, inferSchema=True)

fn = "planinformation.txt"
file_path = os.path.join(fp, fn)
plan_info_df = spark.read.csv(
    file_path, sep="|", header=True, inferSchema=True)

# Example: Filter data based on selected RXCUI and Tier Level


def filter_data(rxcui, tier_level):
    filtered_df = basic_formulary_df.filter(
        (col("RXCUI") == rxcui) & (col("TIER_LEVEL_VALUE") == tier_level))
    return filtered_df


# Example usage
rxcui = "123456"  # Replace with actual RXCUI
tier_level = "2"  # Replace with actual tier level
filtered_data = filter_data(rxcui, tier_level)


# Aggregate data by tier level
tier_distribution = filtered_data.groupBy(
    "TIER_LEVEL_VALUE").count().toPandas()

# Create bar chart
fig = px.bar(tier_distribution, x="TIER_LEVEL_VALUE", y="count",
             title="Formulary Tier Distribution",
             labels={"TIER_LEVEL_VALUE": "Tier Level", "count": "Number of Plans"})
fig.show()


# Join geographic data with formulary data
geo_coverage_df = basic_formulary_df.join(
    geographic_locator_df, on="COUNTY_CODE").groupBy("STATENAME").count().toPandas()

# Create choropleth map
fig = px.choropleth(geo_coverage_df, locations="STATENAME", locationmode="USA-states",
                    color="count", scope="usa",
                    title="Geographic Coverage by State",
                    labels={"count": "Number of Plans"})
fig.show()


# Filter beneficiary cost data for the selected drug
cost_data = beneficiary_cost_df.filter(col("RXCUI") == rxcui).select(
    "COST_AMT_PREF", "COST_AMT_NONPREF", "COST_AMT_MAIL_PREF", "COST_AMT_MAIL_NONPREF").toPandas()

# Create box plot
fig = px.box(cost_data, title="Cost-Sharing Analysis",
             labels={"value": "Cost Amount", "variable": "Cost Type"})
fig.show()


# Aggregate data by plan type
plan_coverage = plan_info_df.groupBy("PLAN_NAME").count().toPandas()

# Create pie chart
fig = px.pie(plan_coverage, values="count", names="PLAN_NAME",
             title="Plan Coverage Distribution")
fig.show()


# Streamlit app
st.title("Pharmaceutical Analysis Dashboard")

# Input features
rxcui = st.text_input("Enter RXCUI", "123456")
tier_level = st.selectbox("Select Tier Level", ["1", "2", "3", "4", "5"])

# Filter data
filtered_data = filter_data(rxcui, tier_level)

# Display visualizations
if st.button("Show Formulary Tier Distribution"):
    tier_distribution = filtered_data.groupBy(
        "TIER_LEVEL_VALUE").count().toPandas()
    fig = px.bar(tier_distribution, x="TIER_LEVEL_VALUE", y="count",
                 title="Formulary Tier Distribution",
                 labels={"TIER_LEVEL_VALUE": "Tier Level", "count": "Number of Plans"})
    st.plotly_chart(fig)

if st.button("Show Geographic Coverage Map"):
    geo_coverage_df = basic_formulary_df.join(
        geographic_locator_df, on="COUNTY_CODE").groupBy("STATENAME").count().toPandas()
    fig = px.choropleth(geo_coverage_df, locations="STATENAME", locationmode="USA-states",
                        color="count", scope="usa",
                        title="Geographic Coverage by State",
                        labels={"count": "Number of Plans"})
    st.plotly_chart(fig)
