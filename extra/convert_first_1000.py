import os
import pandas as pd
import subprocess


def count_lines_wc(file_path):
    print(file_path)
    result = subprocess.run(['wc', '-l', file_path],
                            capture_output=True, text=True)
    return int(result.stdout.split()[0])


def convert_text_to_excel(n):
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    for file in os.listdir(script_dir):
        if file.endswith(".txt"):
            file_path = os.path.join(script_dir, file)
            excel_filename = f"{file[0:-4]}.xlsx"
            excel_path = os.path.join(script_dir, excel_filename)
            try:
                total_lines = count_lines_wc(file_path)
                # Read only the first n lines
                with open(file_path, 'r', encoding='utf-8') as file:

                    lines_to_read = min(total_lines, n)

                    lines = [next(file)
                             for _ in range(lines_to_read)]  # Read first n lines

                # Convert lines into a DataFrame
                df = pd.DataFrame([line.strip().split('|')
                                  for line in lines[:lines_to_read]])

                # Convert lines into a DataFrame
                # df = pd.DataFrame([line.strip().split('|') for line in lines])

                # Set the first row as column headers
                df.columns = df.iloc[0]  # First row as headers
                # Remove the first row from data
                df = df[1:].reset_index(drop=True)

                # Save to Excel
                df.to_excel(excel_path, index=False)
                print(f"Excel file saved successfully: {excel_path}")

            except FileNotFoundError:
                print("Error: File not found.")
            except Exception as e:
                print(f"Error: {e}")


# Example usage
# Convert first 10 lines
convert_text_to_excel(1000)
# count_lines_wc("c:\Users\AMSHU\Downloads\CODEFest\MonthlyPrescriptionDrugPlanFormularyandPharmacyNetworkInformation\2025-01\2025_20250123\planinformation20250131.txt")
