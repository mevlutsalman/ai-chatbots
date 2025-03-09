import streamlit as st  # Web uygulaması oluşturmak için Streamlit kullanıyoruz
from PyPDF2 import PdfReader  # PDF dosyasından metin okumak için kullanılıyor
import pdfplumber  # PDF içeriğini daha iyi işleyebilmek için kullanılıyor
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Metni küçük parçalara ayırmak için
from langchain.embeddings.openai import OpenAIEmbeddings  # OpenAI'nin metinleri vektör haline getiren aracı
from langchain.vectorstores import FAISS  # Hızlı arama yapabilmek için vektör veritabanı
from langchain.chains.question_answering import load_qa_chain  # Sorulara cevap verebilmek için
from langchain.chat_models import ChatOpenAI  # OpenAI'nin dil modeli ile konuşmak için

# OpenAI API Anahtarı (Güvenlik için çevre değişkeni olarak saklanmalı)
OPENAI_API_KEY = "*******************************************************************************"

# Uygulamanın başlığı
st.header("MEV'S ISTQB AI TESTING EXAM PREP")  

# Kullanıcının soru gireceği alan
user_question = st.text_input("Type Your question here")

# Yan panel (PDF yükleme bölümü)
with st.sidebar:
    st.title("Your Document")  
    file = st.file_uploader("Upload a PDF file and start asking questions", type="pdf")  # PDF dosyası yükleme

# Eğer kullanıcı bir dosya yüklediyse, içeriğini okuyalım
if file is not None:
    text = ""  # PDF içeriğini saklamak için boş bir metin değişkeni oluşturduk
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()  # Sayfadaki metni çıkar
            if extracted_text:
                text += extracted_text + "\n"  # Metni birleştirerek sakla
    
    st.sidebar.write(text)  # Kullanıcıya PDF içeriğini göster

    # Metni küçük parçalara bölelim (Büyük metinleri işlemek için gereklidir)
    text_splitter = RecursiveCharacterTextSplitter(
        separators="\n",  # Satır bazlı ayırma
        chunk_size=3000,  # Her parçanın maksimum 3000 karakter olması
        chunk_overlap=150,  # Parçalar arasında 150 karakterlik bir örtüşme olsun
        length_function=len  # Uzunluğu ölçmek için Python'un len fonksiyonunu kullan
    )
    chunks = text_splitter.split_text(text)  # Metni parçalara ayır

    st.write(chunks)  # Bölünmüş metin parçalarını ekranda göster

    # OpenAI'nin metinleri vektör haline getirmesi için embeddings oluşturuyoruz
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    
    # FAISS kullanarak vektör veritabanı oluşturuyoruz (Bu sayede metin içinde hızlı arama yapabiliriz)
    vector_store = FAISS.from_texts(chunks, embeddings)
    
    user_question = st.text_input("Type Your question here")  # Kullanıcının sorusunu al

    # Kullanıcı bir soru sorduğunda çalıştır
    if user_question:
        match = vector_store.similarity_search(user_question, k=3)  # En alakalı 3 parçayı bul
        
        # OpenAI dil modelini başlat
        llm = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,  # API anahtarını kullan
            temperature=0,  # Cevapların daha tutarlı olması için rastgeleliği kapat
            max_tokens=1000,  # Maksimum 1000 kelimeyle cevap ver
            model_name="gpt-3.5-turbo"  # Kullanılan modelin adı
        )
        
        # Sorulan soruya uygun cevabı oluşturacak bir işlem zinciri başlatıyoruz
        chain = load_qa_chain(llm, chain_type="stuff")
        response = chain.run(input_documents=match, question=user_question)  # Modelin cevabını al
        
        st.write(response)  # Ekranda cevabı göster
