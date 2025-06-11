import streamlit as st
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

# Load .env and secret token
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Init grammar correction client (smaller model)
grammar_client = InferenceClient(
    model="vennify/t5-base-grammar-correction",
    token=HF_TOKEN
)

# Init tone transformation client (larger model)
tone_client = InferenceClient(
    model="google/flan-t5-xl",
    token=HF_TOKEN
)

# UI config
st.set_page_config(page_title="Hybrid Text Enhancer", layout="wide")
st.title("🧠 Hybrid Text Enhancer (via Hugging Face InferenceClient)")
st.markdown("First, grammar correction → then optionally enhance tone using large models on Hugging Face.")

# User input
text_input = st.text_area("✍️ Enter your text:", height=200)

tone = st.selectbox(
    "🎨 Choose a transformation tone:",
    (
        "None (just grammar correction)",
        "Formal",
        "Friendly",
        "Simplified",
        "Poem",
        "Rhymes",
        "Dramatic",
        "Electric",
        "Horror",
        "Storytelling"
    )
)

# Enhance button
if st.button("🚀 Enhance Text"):
    if not text_input.strip():
        st.warning("Please enter some text.")
    else:
        try:
            # Step 1: Grammar correction
            with st.spinner("🧹 Correcting grammar..."):
                corrected = grammar_client.text_generation(
                    text_input,
                    max_new_tokens=256,
                    do_sample=False
                )
                corrected_text = corrected.strip()

            # Step 2: Tone enhancement
            if tone == "None (just grammar correction)":
                refined_text = corrected_text
            else:
                with st.spinner(f"🎭 Applying tone: {tone}"):
                    tone_prompts = {
                        "Formal": f"Rewrite formally: {corrected_text}",
                        "Friendly": f"Rewrite to sound friendly and casual: {corrected_text}",
                        "Simplified": f"Rewrite using simpler words: {corrected_text}",
                        "Poem": f"Rewrite this as a beautiful poem: {corrected_text}",
                        "Rhymes": f"Rewrite this text with rhyming lines: {corrected_text}",
                        "Dramatic": f"Rewrite this text dramatically, with emotion and suspense: {corrected_text}",
                        "Electric": f"Rewrite this with energetic, exciting language: {corrected_text}",
                        "Horror": f"Rewrite this like a horror story: {corrected_text}",
                        "Storytelling": f"Retell this as an engaging short story: {corrected_text}",
                    }
                    tone_prompt = tone_prompts[tone]
                    transformed = tone_client.text_generation(
                        tone_prompt,
                        max_new_tokens=512,
                        do_sample=False
                    )
                    refined_text = transformed.strip()

            # Output
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📝 Corrected Text")
                st.warning(corrected_text)
            with col2:
                st.subheader("🎨 Enhanced Output")
                st.success(refined_text)

        except Exception as e:
            st.error(f"❌ Error: {e}")
