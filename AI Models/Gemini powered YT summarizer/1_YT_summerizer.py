import streamlit as st
from langchain.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import re
import os
import json
from pathlib import Path
from datetime import datetime

load_dotenv()

# Initialize models
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)

# Constants
DB_DIR = "LANGCHAIN_rag"
DB_PATH = os.path.join(DB_DIR, "faiss_db")
VIDEO_METADATA_PATH = os.path.join(DB_DIR, "video_metadata.json")

video_id = summary = answer  = None

# Ensure directories exist
Path(DB_DIR).mkdir(parents=True, exist_ok=True)

# Helper functions
def get_video_id(url):
    """Extract video ID from YouTube URL"""
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    
    match = re.search(youtube_regex, url)
    if match:
        return match.group(6)
    return None

def save_video_metadata(**data):
    """Save video metadata for future reference"""
    metadata = {
        "video_id": data.get("video_id"),
        "url": data.get("url"),
        "summery": "",
        "questions": "",
        "answers": ""
    }
    
    if os.path.exists(VIDEO_METADATA_PATH):
        with open(VIDEO_METADATA_PATH, 'r') as f:
            existing_data = json.load(f)

        for k,v in data.items():
            existing_data[k] = v
    else:
        existing_data = metadata
    
    with open(VIDEO_METADATA_PATH, 'w') as f:
        json.dump(existing_data, f, indent=4)

def load_last_video_metadata():
    """Load video metadata for future reference"""
    if os.path.exists(VIDEO_METADATA_PATH):
        with open(VIDEO_METADATA_PATH, 'r') as f:
            try:
                return json.load(f)
            except Exception as e:
                pass
    return {}

def indexing(video_id, url):
    """Index YouTube video transcript"""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        transcript = " ".join([d["text"] for d in transcript_list])
        
        # text splitter
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.create_documents([transcript])
        
        # embedding
        vector_store = FAISS.from_documents(chunks, embedding_model)
        
        # save vector store
        vector_store.save_local(DB_PATH)
        
        # save video metadata
        save_video_metadata(video_id=video_id, url=url)
        
        return True
    except TranscriptsDisabled:
        st.error("Transcript is disabled for this video")
        return False
    # except Exception as e:
    #     st.error(f"An error occurred: {str(e)}")
    #     return False

def load_vector_store():
    """Load existing vector store if available"""
    try:
        if os.path.exists(DB_PATH):
            return FAISS.load_local(DB_PATH, embedding_model, allow_dangerous_deserialization=True)
        return None
    except Exception as e:
        st.error(f"Error loading vector store: {str(e)}")
        return None

def get_summary(vector_store, question):
    """Generate summary from vector store"""
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="You are a helpful assistant. Answer the question based on the given context.\n\nContext: {context}\n\nQuestion: {question}"
    )

    chain = RunnableParallel(
        {
            "context": vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4}) | RunnableLambda(lambda r: "\n\n".join([doc.page_content for doc in r])),
            "question": RunnablePassthrough()
        }
    ) | prompt_template | llm | StrOutputParser()

    return chain.invoke(question)

def main():
    global video_id, summary, answer
    st.title("YouTube Video Summarizer")
    
    # Load existing vector store
    vector_store = load_vector_store()
    
    # Sidebar for video processing
    st.sidebar.header("Video Processing")
    youtube_url = st.sidebar.text_input("Enter YouTube URL:", load_last_video_metadata().get("url","None"))
    
    if st.sidebar.button("Process Video"):

        if youtube_url:
            video_id = get_video_id(youtube_url)
            if video_id:
                with st.spinner("Indexing video transcript..."):
                    success = indexing(video_id, youtube_url)
                    if success:
                        vector_store = load_vector_store()
            else:
                st.sidebar.error("Invalid YouTube URL. Please enter a valid YouTube URL.")
        else:
            st.sidebar.warning("Please enter a YouTube URL")

    # load the saved current video id
    try:
        video_id = load_last_video_metadata().get("video_id")
        if video_id:
            st.sidebar.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)
    except Exception as e:
        st.sidebar.error(f"Error loading video thumbnail: {str(e)}")

    # Main content area
    if vector_store:
        st.info("Vector store loaded. You can now ask questions about the video.")
        
        # Show video summary
        if st.button("Show Video Summary"):
            with st.spinner("Generating summary..."):
                summary = get_summary(vector_store, "please summarize the video transcript")
                save_video_metadata(summery=summary)

        st.write("### Video Summary:")
        st.write(summary if summary else load_last_video_metadata().get("summery",""))

        # Question answering
        question = st.text_input("Ask a question about the video:", load_last_video_metadata().get("questions",""))
        if st.button("Ask") and question:
            with st.spinner("Generating answer..."):
                answer = get_summary(vector_store, question)
                save_video_metadata(questions=question, answers=answer)

        st.write("### Answer:")
        st.write(answer if answer else load_last_video_metadata().get("answers",""))
    else:
        st.info("Please process a video first to start asking questions.")

if __name__ == "__main__":
    main()