from dotenv import load_dotenv
import streamlit as st
from openai import AzureOpenAI, OpenAI
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
import zipfile
from langchain_community.document_loaders import PyPDFLoader
import ast 
import base64


load_dotenv()
AZURE_OPENAI_KEY = "AZURE_OPENAI_API_KEY"
AZURE_OPENAI_ENDPOINT = "AZURE_OPENAI_ENDPOINT"
MODEL_NAME = "MODEL_NAME"


st.markdown("<h1 style='text-align: center;'>Legal Assistant</h1>", unsafe_allow_html=True)


client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2023-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )


def convert_text_to_speech(input_text):

    # Specify the path for the output audio file
    speech_file_path = r"C:/Users/ybaronadao/Documents/Hackathon/local_multimodal_ai_chat/audio/speech.mp3"

    try:
        # Call OpenAI's API to generate speech from text
        response = OpenAI().audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=input_text
        )
        
        # Stream the response to a file
        response.stream_to_file(speech_file_path)
        
        return speech_file_path
    
    except Exception as e:
        st.error(f"Failed to convert text to speech: {e}")
        return None

def create_zip(documents):
    doc_list_corrected = ast.literal_eval(documents) if isinstance(documents, str) else documents
    zip_filename = "documents.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as myzip:
        for document in doc_list_corrected:
            full_path = rf"C:\Users\ybaronadao\Documents\Hackathon\local_multimodal_ai_chat\documents\{document}"
            myzip.write(full_path, arcname=document)
    return zip_filename


def search_documents(prompt):
    loader = PyPDFLoader(r"C:/Users/ybaronadao/Documents/Hackathon/local_multimodal_ai_chat/documents/Divorce in Belgium_ a guide for separating couples _ Expatica.pdf")
    pages = loader.load_and_split()
    faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings())
    docs = faiss_index.similarity_search(prompt, k=2)
    concatenated_results = ""
    for doc in docs:
        concatenated_results + "|" + str(doc.metadata["page"]) + doc.page_content
    return concatenated_results

def check_procedure(prompt):
    procedure = client.chat.completions.create(
            model="SearchEngine",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": """Based on the following input: "Hello, i would like to get assistant about divorce. I want to know if i can do that without lawyers, is it possible?". Define to which legal procedures present in this list does the input belong ['Divorce','Theaft', 'Robery']. Reply only with the name of the procedure and nothing else """},
        {"role": "assistant", "content": "Divorce"},
        {"role": "user", "content": f"""Based on the following input: "{prompt}". Define to which legal procedures present in this list does the input belong ['Divorce','Theaft', 'Robery']. Reply only with the name of the procedure and nothing else """}
            ])
    return procedure.choices[0].message.content

def check_documents(prompt):
    doc_info = search_documents(prompt)
    files = ["Application Form for Divorce.docx", "Mutual Agreement Document Template.docx", "How to buy a houes.docx", "How to appeal court.docx", "Temaplte of tax submission.docx"]
    documents = client.chat.completions.create(
            model="SearchEngine",
            messages=[
                {"role": "system", "content": "you are an assistant that don't reply in natural language, only output allowed is a python list"},
        {"role": "user", "content": """Based on the following input: "Hello, i would like to get assistant about divorce. I want to know if i can do that without lawyers, is it possible?" and the following information "In order for you to get divorce in Belgium you will need:-Identification -Residency permit information 
         -Formal petition for divorce -Agreement on how to deal with issues arising -Pre-nuptial agreement (huwelijkscontract / contrat de mariage), if one exists -Income, property and tax information -Information about any children -A parenting plan, if there are children involved".
         Which if the documents from the following list can be usefule templates to help me?. ["Application Form for Divorce.docx", "Mutual Agreement Document Template.docx", "How to buy a houes.docx", "How to appeal court.docx", "Temaplte of tax submission.docx"]. Your output must be python list python list including the useful documents. For example["Application Form for Divorce.docx", "Mutual Agreement Document Template.docx", "How to buy a houes.docx", "How to appeal court.docx", "Temaplte of tax submission.docx"] """},
        {"role": "assistant", "content": """["Application Form for Divorce.docx", "Mutual Agreement Document Template.docx"]"""},
        {"role": "user", "content": """Based on the following input: "Hello, i would like to get assistant about divorce. I want to know if i can do that without lawyers, is it possible?" and the following information "In order for you to get divorce in Belgium you will need:-Identification -Residency permit information 
         -Formal petition for divorce -Agreement on how to deal with issues arising -Pre-nuptial agreement (huwelijkscontract / contrat de mariage), if one exists -Income, property and tax information -Information about any children -A parenting plan, if there are children involved".
         Which if the documents from the following list can be usefule templates to help me?. ["Application Form for Divorce.docx", "Mutual Agreement Document Template.docx", "How to buy a houes.docx", "How to appeal court.docx", "Temaplte of tax submission.docx"]. Your output must be python list including the useful documents. For example["Application Form for Divorce.docx", "Mutual Agreement Document Template.docx", "How to buy a houes.docx", "How to appeal court.docx", "Temaplte of tax submission.docx"] """},
        {"role": "assistant", "content": """["Application Form for Divorce.docx", "Mutual Agreement Document Template.docx"]"""},
        {"role": "user", "content": f"""Based on the following input: "{prompt}" and the following information {doc_info}.Which if the documents from the following list can be usefule templates to help me? {files}. Reply only with the python list including the useful documents"""}
            ])
    return(documents.choices[0].message.content, doc_info)

toggle = st.sidebar.toggle('Audio assitant')

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.procedure = None
    st.session_state.explaination = None
    st.session_state.doc_list = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can i help you"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        inference = []
        inference = [{"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages]
# Interaction starts
        
        if st.session_state.procedure == None:
            st.session_state.procedure = check_procedure(prompt)

        doc_list , doc_search = check_documents(prompt)
        st.session_state.doc_list = doc_list

        if st.session_state.doc_list == []:
            inference.append({"role": "user", "content": "Repete this exact words: Im sorry, i couldn't find any document that can be helpfull "})
        else:    
            zipfilename = create_zip(doc_list)
            few_shots = [
                {"role": "system", "content": "You are a helpful legal assistant."},
                {"role": "user", "content": """Based on the following input: "Hello, i would like to get assistant about divorce. I want to know if i can do that without lawyers, is it possible?. We don't have children" and the following list of document templates ["Application Form for Divorce.docx", "Mutual Agreement Document Template.docx"]
                Reply kindly mentioning that these are the documents you found and that they are available for download. And  based on the following information "In order for you to get divorce in Belgium you will need:-Identification -Residency permit information 
                -Formal petition for divorce -Agreement on how to deal with issues arising -Pre-nuptial agreement (huwelijkscontract / contrat de mariage), if one exists -Income, property and tax information -Information about any children -A parenting plan, if there are children involved", remind the user of other documents he could need """},
                {"role": "assistant", "content": """Hello, here is the list of template documents that are helpful to you: 1.Application Form for Divorce 2.Mutual Agreement Document Template. They are available for download. Please remember that based on your case you may also need -Pre-nuptial agreement (huwelijkscontract / contrat de mariage)"""},
                {"role": "user", "content": f"""Based on the following input: {prompt} and the following list of document templates {doc_list}
                Reply kindly mentioning that these are the documents you found and that they are available for download. And  based on the following information {doc_search}, remind the user of other documents he could need """}
                    ]
            inference.extend(few_shots)
            stream  = client.chat.completions.create(
                model="SearchEngine",
                messages=inference)
            response = st.write(stream.choices[0].message.content)
            with open(zipfilename, 'rb') as f:
                st.download_button('Download Zip', f, file_name='archive.zip')

            if toggle:
                speech_file_path = convert_text_to_speech(stream.choices[0].message.content)
                autoplay_audio(speech_file_path)

    st.session_state.messages.append({"role": "assistant", "content": stream.choices[0].message.content})
