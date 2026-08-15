# RAG AI Chatbot



A Retrieval-Augmented Generation (RAG) chatbot that allows users to upload a PDF document and ask questions about its content.



## Features



- Upload and process PDF documents

- Split document text into smaller chunks

- Generate embeddings using Hugging Face

- Store and search embeddings using FAISS

- Retrieve relevant information based on the user's question

- Generate natural-language answers using OpenAI

- Interactive web interface built with Streamlit



## How It Works



PDF → Text → Text Chunks → Embeddings → FAISS Vector Store → Relevant Chunks → OpenAI → Answer



1. The user uploads a PDF.

2. The application extracts the text.

3. The text is divided into smaller chunks.

4. Hugging Face converts the chunks into embeddings.

5. FAISS stores and searches the embeddings.

6. The most relevant information is retrieved for the user's question.

7. OpenAI uses the retrieved information to generate an answer.



## Technologies Used



- Python

- Streamlit

- LangChain

- FAISS

- Hugging Face Sentence Transformers

- OpenAI API



## Example



**Question:** How many vacation days do employees receive?



**Answer:** Employees receive 15 days of paid vacation each calendar year.



## Project Purpose



This project demonstrates how Retrieval-Augmented Generation can combine document retrieval with a large language model to answer questions using information from a specific document.
