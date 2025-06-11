# MUST be the first Streamlit command
import streamlit as st
st.set_page_config(page_title="Hybrid Text Enhancer", layout="wide")

from happytransformer import HappyTextToText, TTSettings
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch


# === Grammar Correction using HappyTransformer ===
happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
args = TTSettings(num_beams=5, min_length=1)

def fix_grammar(text):
    return happy_tt.generate_text(f"grammar:{text}", args=args).text

# === Tone Model Loader using transformers pipeline ===
@st.cache_resource
def load_tone_model(device_str: str):
    model_id = "google/flan-t5-xl"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id).to(device_str)
    return pipeline("text2text-generation", model=model, tokenizer=tokenizer, device=0 if device_str == "cuda" else -1)


# Tone prompt dictionary
tone_prompts = {
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
st.title("🧠 Hybrid Text Enhancer (FLAN on GPU)")
st.markdown("First, grammar correction → then optionally enhance tone using FLAN-T5 on GPU (if available).")

initial_text = "I has a apple. I like to play football with my friends. The weather is nice to0day."
text_input = st.text_area("✍️ Enter your text:", value=initial_text, height=200)

tone = st.selectbox(
    "🎨 Choose a transformation tone:",
    ["None (just grammar correction)"] + list(tone_prompts.keys())
)

device_str = st.selectbox(
    "🔧 Select device for tone generation:",
    ["cpu", "cuda" if torch.cuda.is_available() else "cpu"]
)

# Load model with correct device
tone_generator = load_tone_model(device_str)


if st.button("🚀 Enhance Text"):
    if not text_input.strip():
        st.warning("Please enter some text.")
    else:
        try:
            # Step 1: Grammar correction
            with st.spinner("🧹 Correcting grammar..."):
                corrected_text = fix_grammar(text_input)

            # Step 2: Tone enhancement
            if tone == "None (just grammar correction)":
                refined_text = corrected_text
            else:
                with st.spinner(f"🎭 Applying tone: {tone}"):
                    prompt = f"{tone_prompts[tone]} {corrected_text}"
                    output = tone_generator(prompt, max_new_tokens=128, do_sample=False)
                    refined_text = output[0]["generated_text"].strip()

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
