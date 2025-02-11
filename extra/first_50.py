import os


def display_first_50_lines(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file):
                if i >= 50:
                    break
                print(line, end='')  # Avoids extra new lines
    except FileNotFoundError:
        print("Error: File not found.")
    except Exception as e:
        print(f"Error: {e}")


# Replace with your file path
file_path = os.path.dirname(os.path.abspath(__file__))
file_name = "beneficiary cost file  20250131.txt"

full_file_path = os.path.join(file_path, file_name)

print(full_file_path)

display_first_50_lines(full_file_path)
