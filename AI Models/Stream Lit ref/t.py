# MUST be the first Streamlit command
import streamlit as st
st.set_page_config(page_title="Hybrid Text Enhancer (Gemini)", layout="wide")

import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Prompt templates
TONE_PROMPTS = {
    "Formal": "Please rewrite the following text in a formal tone:",
    "Professional": "Please rewrite the following text to sound professional and polished:",
    "Friendly": "Please rewrite the following text to sound friendly, warm, and casual:",
    "Simplified": "Please rewrite the following text using simpler words and clearer language:",
    "Poem": "Please turn the following text into a beautiful and expressive poem:",
    "Rhymes": "Please rewrite the following text so that it rhymes like a poem or song:",
    "Dramatic": "Please rewrite the following text with intense emotion and dramatic flair:",
    "Electric": "Please rewrite the following text with high energy and excitement:",
    "Horror": "Please rewrite the following text as a chilling and suspenseful horror story:",
    "Storytelling": "Please rewrite the following text as a vivid and engaging short story:"
}

# === Streamlit UI ===
st.title("🧠 Hybrid Text Enhancer (Gemini)")
st.markdown("This app performs grammar correction and optional tone transformation using Google Gemini Pro.")

initial_text = "I has a apple. I like to play football with my friends. The weather is nice to0day."
text_input = st.text_area("✍️ Enter your text:", value=initial_text, height=200)

tone = st.selectbox(
    "🎨 Choose a transformation tone:",
    ["None (just grammar correction)"] + list(TONE_PROMPTS.keys())
)

# Enhance button
if st.button("🚀 Enhance Text"):
    if not text_input.strip():
        st.warning("Please enter some text.")
    else:
        try:
            # Step 1: Grammar correction
            with st.spinner("🧹 Correcting grammar..."):
                grammar_prompt = f"Correct the grammar of the following text:\n\n{text_input}"
                grammar_response = model.generate_content(grammar_prompt)
                corrected_text = grammar_response.text.strip()

            # Step 2: Tone enhancement
            if tone == "None (just grammar correction)":
                refined_text = corrected_text
            else:
                with st.spinner(f"🎭 Applying tone: {tone}"):
                    tone_prompt = f"{TONE_PROMPTS[tone]}\n\n{corrected_text}"
                    tone_response = model.generate_content(tone_prompt)
                    refined_text = tone_response.text.strip()

            # Display output
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📝 Corrected Text")
                st.success(corrected_text)
            if tone != "None (just grammar correction)":
                with col2:
                    st.subheader("🎨 Enhanced Output")
                    st.success(refined_text)

        except Exception as e:
            st.error(f"❌ Error: {e}")
