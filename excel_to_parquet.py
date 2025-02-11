import os
import pandas as pd


def convert_excel_to_parquet(folder_path):
    """
    Converts all .xlsx files in the given folder to Parquet format.
    """
    for file in os.listdir(folder_path):
        if file.endswith("formulary_file.xlsx"):
            excel_path = os.path.join(script_dir, file)
            parquet_path = excel_path.replace(".xlsx", ".parquet")

            # Convert Excel to Parquet for speed optimization
            if not os.path.exists(parquet_path):
                print("Converting Excel to Parquet for faster access...")
                df = pd.read_excel(excel_path, engine="openpyxl")
                df.to_parquet(parquet_path, index=False)


if __name__ == "__main__":
    # folder = input("Enter the folder path: ").strip()
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Convert Excel files to Parquet
    convert_excel_to_parquet(script_dir)
