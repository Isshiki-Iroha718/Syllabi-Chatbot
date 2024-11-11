import os
from database import extract, update

def read_files_in_directory(directory_path):
    extracted_data = []

    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith(".pdf"):
                file_path = os.path.join(root, file_name)
                update(extract(file_path))

    return extracted_data

directory = "Syllabus/Syllabi/"

results = read_files_in_directory(directory)
