import streamlit as st
from PyPDF2 import PdfReader
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI

# OpenAI API Key
OPENAI_API_KEY = "*******************************************************************************"

# Başlık
st.header("MEV'S ISTQB AI TESTING EXAM PREP")  

user_question = st.text_input("Type Your question here")

# Yan panelde başlık
with st.sidebar:
    st.title("Your Document")  
    file = st.file_uploader("Upload a PDF file and start asking questions", type="pdf") 

# Metni çıkar
if file is not None:
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
    
    st.sidebar.write(text)
    
    # Metni parçala 
    text_splitter = RecursiveCharacterTextSplitter(
        separators="\n",
        chunk_size=3000,
        chunk_overlap=150,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    
    st.write(chunks)

    # OpenAI Embeddings oluştur
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    
    # FAISS vektör deposu oluştur
    vector_store = FAISS.from_texts(chunks, embeddings)
    
    user_question = st.text_input("Type Your question here")
    
    # Kullanıcı soru sorduğunda çalıştır
    if user_question:
        match = vector_store.similarity_search(user_question, k=3)
        
        # LLM Modeli tanımla
        llm = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            temperature=0,
            max_tokens=1000,
            model_name="gpt-3.5-turbo"
        )
        
        # Cevabı oluştur
        chain = load_qa_chain(llm, chain_type="stuff")
        response = chain.run(input_documents=match, question=user_question)
        
        st.write(response)