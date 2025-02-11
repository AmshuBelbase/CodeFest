import os
import pandas as pd

# Get the directory where the script is located
folder_path = os.path.dirname(os.path.abspath(__file__))
print(folder_path)

# Ensure Pandas displays all columns
pd.set_option("display.max_columns", None)

# Get a list of all Excel files in the folder
excel_files = [f for f in os.listdir(folder_path) if f.endswith(".xlsx")]
print(excel_files)
# Loop through each Excel file and print the first 5 lines
for file in excel_files:
    file_path = os.path.join(folder_path, file)
    try:
        df = pd.read_excel(file_path)  # Read Excel file
        print("\n")
        print(file_path)
        print(f"--- First 5 lines of {file} ---")
        print(df.head(5))  # Print first 5 rows
    except Exception as e:
        print(f"Error reading {file}: {e}")
