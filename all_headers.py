import os
import pandas as pd


def print_headers():
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    for file in os.listdir(script_dir):
        if file.endswith(".xlsx"):
            file_path = os.path.join(script_dir, file)
            try:
                # Read only the first row (header)
                df = pd.read_excel(file_path, nrows=0)

                # Print file name and its header
                print(f"File: {file}\nHeader: {', '.join(df.columns)}\n")

            except Exception as e:
                print(f"Error reading {file}: {e}")


# Run the function
print_headers()
