import os
from database import extract, update

def read_files_in_directory(directory_path):
    count = 0
    extracted_data = []

    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith(".pdf"):
                file_path = os.path.join(root, file_name)
                update(extract(file_path))
                count = count + 1

    print("There are " + str(count) + " syllabus files handled.")
    return extracted_data

# Change the directory prefix if needed
directory = "static/Syllabus/"

results = read_files_in_directory(directory)
