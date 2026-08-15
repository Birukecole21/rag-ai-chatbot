import streamlit as st                                                                       
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
llm = ChatOpenAI(
    model="gpt-4o-mini"
)
st.title("RAG Chatbot")
st.write("Upload a PDF and ask a question about it.")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    st.success("PDF uploaded successfully!")
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
        st.write(text)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_text(text)
    #st.write(f"Created {len(chunks)} text chunks.")
    # Load the embeddings model
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # convert the chunks into embeddings
    chunk_embeddings = embeddings.embed_documents(chunks)
    #st.write(f"Created embeddings for {len(chunk_embeddings)} chunks.")
    # Create a FAISS vector store from the embeddings

    vector_store = FAISS.from_texts(
        texts=chunks,
        embedding=embeddings    
    )
    retriever = vector_store.as_retriever()

    question = st.text_input("Ask a question about the PDF:")
    if question:
        results = retriever.invoke(question)

        context = "\n\n".join(
            [doc.page_content for doc in results]
        )

        prompt = f"""
        Answer the question only using the context below.

        Context: {context}

        Question: {question}
        """
    try:
        with st.spinner("Generating answer..."):
                response = llm.invoke(prompt)

        st.write("Answer:")
        st.write(response.content)
    except Exception as e:
        st.error("something went wrong while generating the answer. Please try again.")