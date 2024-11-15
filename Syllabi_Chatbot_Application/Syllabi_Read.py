from langchain_community.document_loaders import TextLoader, PyPDFLoader,UnstructuredWordDocumentLoader
import os

# Get the file type before import the syllabus file
def get_file_type_by_extension(file_path):
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    if file_extension == '.txt':
        print("File type analysis finished, this file format is TXT")
        return 'txt'
    elif file_extension == '.pdf':
        print("File type analysis finished, this file format is PDF")
        return 'pdf'
    elif file_extension == '.docx':
        print("File type analysis finished, this file format is DOCX")
        return 'docx'
    else:
        print("File type is not supported")
        return 'unknown'

# Read the syllabus information file if the file type is .txt
def read_txt(file_path):
    loader = TextLoader(file_path,
                        encoding='utf-8', autodetect_encoding=True)
    documents = loader.load()
    print("File read successfully")
    return documents

# Read the syllabus information file if the file type is .pdf
def read_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    print("File read successfully")
    return documents

# Read the syllabus information file if the file type is .docx
def read_docx(file_path):
    loader = UnstructuredWordDocumentLoader(file_path)
    documents = loader.load()
    print("File read successfully")
    return documents

# Handle different file types of syllabus information file
def read_file(file_path, file_type):
    if file_type == 'txt':
        return read_txt(file_path)
    elif file_type == 'pdf':
        return read_pdf(file_path)
    elif file_type == 'docx':
        return read_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

# Integrate all methods together to execute
def handle_file(file_path):
    print("Start reading file...")
    file_type = get_file_type_by_extension(file_path)
    return read_file(file_path, file_type)
