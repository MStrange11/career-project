import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Streamlit UI
st.title("Gemini 1.5 Flash Chatbot")
user_input = st.text_input("Ask something:")

if user_input:
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(user_input)
    st.write(response.text)
