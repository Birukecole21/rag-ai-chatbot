import streamlit as st                                                                       
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("🗑️ clear chat"):
    st.session_state.messages = []
    st.rerun()
llm = ChatOpenAI(
    model="gpt-4o-mini"
)
st.set_page_config(
    page_title="RAG PDF Assistant",
    page_icon="📄",
    layout="centered"
)

st.title("📄 RAG PDF Assistant")
st.write(
    "Upload a PDF document and ask questions about its content."
)
# st.write("Upload a PDF and ask a question about it.")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    st.success("PDF uploaded successfully!")
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
        # st.write(text)
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

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    question = st.text_input(
        "💬 Ask a question about your document",
        placeholder="Example: how many vacation days do employees receive?"
    )
    if question:
        results = retriever.invoke(question)
        st.session_state.messages.append(
            {"role": "user", "content": question}
        )

        context = "\n\n".join(
            [doc.page_content for doc in results]
        )

        prompt = f"""
Answer the question only using the context below.

Context: {context}

Question: {question}
"""
        try:
            with st.spinner("🤖 Thinking..."):
                response = llm.invoke(prompt)
            st.session_state.messages.append(
                {"role": "assistant", "content": response.content}
            )

            with st.chat_message("assistant"):
                st.write(response.content)

        except Exception as e:
            st.error("something went wrong while generating the answer. Please try again.")