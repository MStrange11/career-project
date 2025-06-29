# Importing necessary libraries
import os
import streamlit as st
from dotenv import load_dotenv

# LangChain imports
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load environment variables from .env
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Streamlit App Title
st.title("📄 Gemma Model Document Q&A")

# Initialize the LLM using Groq and Gemma model
llm = ChatGroq(groq_api_key=groq_api_key, model_name="gemma2-9b-it")

# Prompt template for answering questions based on context
prompt = ChatPromptTemplate.from_template("""
Answer the question based only on the provided context.
<context>
{context}
</context>

Question: {input}
""")

# Function to load documents, split text, embed, and create vector DB
def vector_embedding():
    if "vectors" not in st.session_state:
        # Load embeddings using Google Generative AI
        st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        # Load all PDFs from a directory
        st.session_state.loader = PyPDFDirectoryLoader("./us_census")
        st.session_state.docs = st.session_state.loader.load()

        # Split documents into manageable chunks
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs)

        # Create FAISS vector store from embedded documents
        st.session_state.vector_store = FAISS.from_documents(
            st.session_state.final_documents, 
            st.session_state.embeddings
        )
        st.session_state.vectors = True  # Mark that vectors are created

# Button to create the vector store
if st.button("Create Vector Store"):
    vector_embedding()
    st.success("✅ Vector store DB is ready!")

# Text input for user question
prompt1 = st.text_input("What do you want to ask from the documents?")

# If user submits a question
if prompt1:
    if "vector_store" in st.session_state:
        # Create document QA chain
        document_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)

        # Create retriever from vector store
        retriever = st.session_state.vector_store.as_retriever()

        # Create final retrieval QA chain
        retrieval_chain = create_retrieval_chain(retriever, document_chain)

        # Run the chain with user input
        with st.spinner("Processing your question..."):
            response = retrieval_chain.invoke({"input": prompt1})
            st.write(response["answer"])
            st.success("Done")
    else:
        st.warning("Please create the vector store first.")