import os
import zipfile


def unzip_all():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(script_dir)

    for file in os.listdir(script_dir):
        print(file)
        if file.endswith(".zip"):
            zip_path = os.path.join(script_dir, file)
            extract_folder = os.path.join(script_dir, os.path.splitext(file)[
                                          0])  # Create folder with zip name
            os.makedirs(extract_folder, exist_ok=True)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_folder)
            print(f"Extracted: {file} -> {extract_folder}")


unzip_all()
