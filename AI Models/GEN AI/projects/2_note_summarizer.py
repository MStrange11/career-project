# project name: Note Summarizer
# description: note summarizer is a study-friendly Streamlit app that takes a PDF as input and returns a summary
#              in Markdown format. It will save the result in a .txt file. 
#              This app also provides an area to ask questions based on the summary.

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import tempfile
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

st.title("Note Summarizer")
st.subheader("Upload your PDF")

pdf = st.file_uploader("Upload your PDF", type="pdf")

prompt = PromptTemplate(
    template=(
        "The following text is extracted from a PDF document. "
        "Read it carefully and create a simple, easy-to-understand topic by topic summary that captures the explanation. "
        "Use Markdown formatting for the output, including:\n"
        "- A short introduction\n"
        "- Main ideas explained clearly\n"
        "- Bullet points for topic by topic explanation and key points\n"
        "- A brief conclusion\n\n"
        "PDF Text:\n{text}"
    ),
    input_variables=["text"]
)


parser = StrOutputParser()
chain = prompt | model | parser

def invoke(chain, data):
    try:
        summary = chain.invoke(data)
        return summary
    except Exception as e:
        st.error(f"Error generating summary: {e}")

if pdf is not None:
    # Save uploaded PDF to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf.read())
        temp_file_path = tmp_file.name

    st.write(f"PDF uploaded: {pdf.name}")

    # Load the PDF
    loader = PyPDFLoader(temp_file_path)
    docs = loader.load()
    combined_text = " ".join([doc.page_content for doc in docs])

    # Generate the summary
    summary = invoke(chain, {"text": combined_text})
    if summary is None:
        with open("projects\summary.txt", "r", encoding="utf-8") as f:
            summary = f.read()

    st.markdown(summary)
    # Save the summary in .txt file
    sub = st.sidebar

    # Q&A Section

    if sub.button("save summary"):

        # Save the result in .txt file
        output_dir = "projects"
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "summary.txt")
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(summary)
        sub.success(f"Summary saved to {output_file}")

    sub.subheader("Q&A about the summary")
    question = sub.text_input("Enter your question about the summary")
    if question:
        qa_prompt = PromptTemplate(
            template=(
                "Carefully read and analyze the following summary. "
                "Based **only** on this summary, provide a clear, accurate, and well-reasoned answer to the user's question. "
                "If the answer is not explicitly stated in the summary, respond with 'Information not available in the summary.'\n\n"
                "Summary:\n{summary}\n\n"
                "Question:\n{question}"
            ),
            input_variables=["summary", "question"]
        )

        qa_chain = qa_prompt | model | parser
        answer = invoke(qa_chain, {"summary": summary, "question": question})
        if answer:
            sub.write(answer)
