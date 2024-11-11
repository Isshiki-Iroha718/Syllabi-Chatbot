from langchain_community.document_loaders import TextLoader
from openai import OpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader("Syllabus/Syllabi/Duhaime MASY1-GC 3220 Information Security Management Fall 2022_Final.txt",
                    encoding='utf-8', autodetect_encoding=True)
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=100,
    separators=["\n\n", ".", " "]
)
# Divided the whole file into different sections
split_documents = text_splitter.split_documents(documents)
documents_list = []

for s in split_documents:
    documents_list.append(s.page_content)

info_str = "\n".join(documents_list)

query = "Tell me about the course?"

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
        {"role": "system", "content": info_str},
        {"role": "user", "content": query}
    ]
)
print(response.choices[0].message.content)
