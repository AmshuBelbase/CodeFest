from pyspark.sql import SparkSession
import os

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Pharmacy Networks Sampling") \
    .getOrCreate()

print("Start")

# Get file path
fp = os.path.dirname(os.path.abspath(__file__))
fn = "pharmacynetworks1.txt"
file_path = os.path.join(fp, fn)

# Load the dataset into a PySpark DataFrame
pharmacy_networks = spark.read.csv(
    file_path, sep="|", header=True, inferSchema=True)

# Get the original size
original_size = pharmacy_networks.count()
print(f"Original size: {original_size}")

# Randomly sample 10% of the data
sampled_data = pharmacy_networks.sample(fraction=0.1, seed=42)

# Get the sampled size
sampled_size = sampled_data.count()
print(f"Sampled size: {sampled_size}")

# Show the first few rows of the sampled data
sampled_data.show(5)

output_file = os.path.join(fp, "sampled_pharmacynetworks.csv")
sampled_data_list = sampled_data.collect()

with open(output_file, "w", encoding="utf-8") as f:
    f.write(",".join(sampled_data.columns) + "\n")  # Write headers
    for row in sampled_data_list:
        f.write(",".join(map(str, row)) + "\n")  # Write rows as CSV

print(f"Sampled data saved at: {output_file}")


# Stop the Spark session
spark.stop()
