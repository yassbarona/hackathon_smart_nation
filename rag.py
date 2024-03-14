from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
import os
load_dotenv()

# Define your directory path
directory_path = r"local_multimodal_ai_chat/documents"

# Initialize an empty list to store your document names
pdf_docs = []

# Check if the directory exists
if os.path.exists(directory_path):
    # Loop through each item in the directory
    for filename in os.listdir(directory_path):
        # Create the full path to the item
        file_path = os.path.join(directory_path, filename)
        # Check if it is a file and not a directory
        if os.path.isfile(file_path):
            # Add the document to the list
            pdf_docs.append(filename)
else:
    print("The directory does not exist.")


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(f"{directory_path}/{pdf}")
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    db_path = r"local_multimodal_ai_chat/faiss_index"
    vectorstore.save_local(db_path)
    result = "OK"
    return result

def add_to_vectors():

    text = get_pdf_text(pdf_docs)
    text_chunks = get_text_chunks(text)
    result = get_vectorstore(text_chunks)
    return(result)

add_to_vectors()