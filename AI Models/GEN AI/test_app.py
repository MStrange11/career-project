import asyncio
import gradio as gr
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

# Fix for missing event loop inside Gradio's worker thread
try:
    asyncio.get_running_loop()
    print("Event loop is running")
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())
    print("Event loop was not running, created a new one")

def process_input(query):
    

    # Embedding
    # embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    # embedding = embedding_model.embed_query(query)

    # LLM Response
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    response = llm.invoke(query)

    # return embedding, response.content
    return response.content


# Gradio interface
demo = gr.Interface(
    fn=process_input,
    inputs=gr.Textbox(label="Enter a query", value="list of ai tools with their founders"),
    outputs=[
        # gr.Textbox(label="Embedding Vector"),
        gr.Textbox(label="LLM Response")
    ],
    title="Gemini Embedding & LLM App",
    description="Returns embeddings and LLM response for the given input."
)

if __name__ == "__main__":
    demo.launch()
