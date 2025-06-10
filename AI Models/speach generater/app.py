import streamlit as st
import base64
import io
import numpy as np
import torch
import soundfile as sf

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from Chatterbox.tts import ChatterboxTTS


# --- App Settings ---
st.set_page_config(page_title="Grammar Refiner + TTS", layout="wide")
st.title("📝 Grammar Refiner + 🎤 Text to Speech Generator")

# --- Load Grammar Correction Model ---
model_name = "prithivida/grammar_error_correcter_v1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
grammar_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
grammar_model.eval()

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
@st.cache_resource
def load_tts_model():
    return ChatterboxTTS.from_pretrained(DEVICE)

tts_model = load_tts_model()

# Initialize session state variables
st.session_state.corrected_text = "The 'Tomb Raider' story primarily focuses on the adventures of Lara Croft, an archaeologist and adventurer. The story usually revolves around her exploration of ancient tombs, ruins, and hazardous locations in search of artifacts and secrets, often facing dangerous challenges and enemies. "
st.session_state.refine_btn = False
if "audio_data" not in st.session_state:
    st.session_state.audio_data = None


def generate_audio(text: str, exaggeration: float = 0.5, temperature: float = 0.8, cfg_weight: float = 0.5):
    st.text("Generating audio...")

    refined_text = text.strip()
    st.text(f"Refined text for TTS: {refined_text[:50]}...")
    if not refined_text:
        st.error("No text provided for Audio generation.")
        return
    try:
        wav = tts_model.generate(
            refined_text,
            exaggeration=exaggeration,
            temperature=temperature,
            cfg_weight=cfg_weight
        )
        sr = tts_model.sr
        wav_np = wav.squeeze(0).numpy()

        audio_buffer = io.BytesIO()
        sf.write(audio_buffer, wav_np, sr, format='WAV')
        st.session_state.audio_data = audio_buffer.getvalue()
        st.success("Audio generation complete!")
        print(f"Generated audio length: {len(st.session_state.audio_data)} bytes")

    except Exception as e:
        st.error(f"Audio generation failed: {e}")

# --- Layout Columns ---
col1, col2 = st.columns([3, 1])

with col1:

    # --- Text Input + Refine Button ---
    with st.container():
        user_input = st.text_area("Enter your text:",value=st.session_state.corrected_text, height=100)
        final_text = user_input.strip()

        col_refine, col_speech = st.columns([1, 1])

        with col_refine:
            if st.button("🔧 Refine", key="refine_button"):
                if user_input.strip():
                    with torch.no_grad():
                        inputs = tokenizer.encode(user_input, return_tensors="pt")
                        outputs = grammar_model.generate(inputs, max_length=128)
                        final_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
                        if final_text:
                            st.session_state.corrected_text = final_text
                            st.session_state.refine_btn = True
                        else:
                            st.warning("No corrections made. Please check your input.")
                else:
                    st.warning("Please enter some text.")

        with col_speech:
                    # --- Parameter Sliders ---
            st.markdown("### 🎛️ TTS Controls")
            exaggeration = st.slider("Exaggeration", min_value=0.25, max_value=2.0, value=0.5, step=0.05)
            cfg_weight = st.slider("CFG Weight", min_value=0.2, max_value=1.0, value=0.5, step=0.05)
            temperature = st.slider("Temperature", min_value=0.05, max_value=5.0, value=0.8, step=0.05)


            if st.button("🎧 Generate Speech", key="generate_button_sidebar"):
                st.session_state.corrected_text = final_text
                generate_audio(st.session_state.corrected_text,exaggeration=exaggeration, temperature=temperature, cfg_weight=cfg_weight)

    # Display Corrected Text
    if st.session_state.refine_btn:
        st.subheader("🪛 Corrections")
        st.text_area("Refined Text:", st.session_state.corrected_text, height=100)

        # Generate TTS Audio
        if st.button("🎧 Generate Speech", key="generate_button_main"):
            generate_audio(st.session_state.corrected_text)

with col2:

    # --- Audio Output + Download ---
    if st.session_state.audio_data:
        st.subheader("🔊 Generated Audio")
        st.audio(st.session_state.audio_data, format="audio/wav")

        b64_audio = base64.b64encode(st.session_state.audio_data).decode()
        href = f'<a href="data:audio/wav;base64,{b64_audio}" download="speech.wav">📥 Download Audio</a>'
        st.markdown(href, unsafe_allow_html=True)
