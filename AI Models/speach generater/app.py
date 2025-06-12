# pip install -r requirements.txt

# Streamlit Grammar Refiner + TTS App using Gemini + Chatterbox

'''
Gemini 1.5 Flash is a variant of Google's Gemini 1.5 family, optimized for speed and efficiency. 
Compared to Gemini 1.5 Pro, which is more powerful and suited for complex reasoning or large-context tasks, Flash is lighter and faster — ideal for use cases like real-time interactions, grammar correction, or tone modulation, where latency and responsiveness matter more than deep reasoning. 
In my app, I used Gemini 1.5 Flash because it provides high-quality language outputs quickly, which is perfect for enhancing text before sending it to the TTS engine.'''


import os
import io
import base64
import tempfile
import requests
import soundfile as sf
import streamlit as st
import torch
import google.generativeai as genai

from dotenv import load_dotenv
from Chatterbox.tts import ChatterboxTTS
from streamlit_audio_recorder import st_audiorec

# --- Configurations ---
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
load_dotenv()
genai.configure(api_key=os.getenv("GMINI_API"))
model = genai.GenerativeModel("models/gemini-1.5-flash")

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# --- Prompt Templates ---
TONE_PROMPTS = {
    "Formal": "Please rewrite the following text in a formal tone",
    "Professional": "Please rewrite the following text to sound professional and polished",
    "Friendly": "Please rewrite the following text to sound friendly, warm, and casual",
    "Simplified": "Please rewrite the following text using simpler words and clearer language",
    "Poem": "Please turn the following text into a beautiful and expressive poem",
    "Rhymes": "Please rewrite the following text so that it rhymes like a poem or song",
    "Dramatic": "Please rewrite the following text with intense emotion and dramatic flair",
    "Electric": "Please rewrite the following text with high energy and excitement",
    "Horror": "Please rewrite the following text as a chilling and suspenseful horror story",
    "Storytelling": "Please rewrite the following text as a vivid and engaging short story",
    "Adventure": "Please rewrite the following text as an exciting and daring adventure story",
    "Logical": "Please rewrite the following text using clear logic and analytical reasoning",
    "Sci-Fi": "Please rewrite the following text as a futuristic science fiction narrative",
    "Mystery": "Please rewrite the following text with an air of suspense and mystery in paragraph form",
    "Motivational": "Please rewrite the following text in a motivational and inspiring tone",
    "Sarcastic": "Please rewrite the following text with a sarcastic and witty twist",
    "News": "Please rewrite the following text in the style of a news report or press release",
    "Academic": "Please rewrite the following text in a scholarly and academic tone"
}

DEFAULT_TEXT = (
    "The 'Tomb Raider' story primarily focuses on the adventures of Lara Croft, "
    "an archaeologist and adventurer. The story usually revolves around her exploration of ancient tombs, ruins, "
    "and hazardous locations in search of artifacts and secrets, often facing dangerous challenges and enemies."
)
DEFAULT_AUDIO_URL = "https://storage.googleapis.com/chatterbox-demo-samples/prompts/female_shadowheart4.flac"

# --- Streamlit Config ---
st.set_page_config(page_title="Grammar Refiner + TTS", layout="wide")

# Info Button UI
with st.container():
    col_info, col_title = st.columns([1, 6])
    with col_info:
        if st.button("ℹ️ Info"):
            st.session_state.show_info = not st.session_state.get("show_info", False)
    with col_title:
        st.title("📝 Grammar Refiner + 🎤 Text to Speech Generator")

if st.session_state.get("show_info"):
    st.markdown("""
    ### ℹ️ App Instructions
    **Workflow:**
    - Enter your base text.
    - Optionally correct grammar and transform tone using Gemini.
    - Choose or record a reference voice.
    - Customize TTS parameters:
        - **Exaggeration**: Emphasizes prosody and emotion.
        - **CFG Weight**: Controls faithfulness to reference audio.
        - **Temperature**: Controls randomness (higher = more creative).
    - Generate speech using Chatterbox.

    **Features:**
    - Grammar correction powered by Gemini 1.5 Flash.
    - 18 tone styles from poetic to sarcastic.
    - Microphone + upload + default voice support.
    - Audio download for refined results.
    """)

# --- Load and Cache TTS Model ---
@st.cache_resource
def load_tts_model():
    return ChatterboxTTS.from_pretrained(DEVICE)

tts_model = load_tts_model()

# --- Session State Initialization ---
if 'corrected_text' not in st.session_state:
    st.session_state.corrected_text = DEFAULT_TEXT
if 'ref_audio_path' not in st.session_state:
    st.session_state.ref_audio_path = None
if 'audio_data' not in st.session_state:
    st.session_state.audio_data = None
if 'exaggeration' not in st.session_state:
    st.session_state.exaggeration = 0.6
if 'cfg_weight' not in st.session_state:
    st.session_state.cfg_weight = 0.3
if 'temperature' not in st.session_state:
    st.session_state.temperature = 0.8

# --- Helpers ---
def refine_text(text: str, tone: str) -> str:
    try:
        grammar_prompt = f"Correct the grammar of the following text:\n\n{text}"
        grammar_response = model.generate_content(grammar_prompt)
        corrected_text = grammar_response.text.strip() if hasattr(grammar_response, "text") else str(grammar_response)

        if tone != "None (just grammar correction)":
            tone_prompt = f"{TONE_PROMPTS.get(tone, '')}. Limit the response to 300 characters.\n\n{corrected_text}"
            tone_response = model.generate_content(tone_prompt)
            corrected_text = tone_response.text.strip() if hasattr(tone_response, "text") else str(tone_response)

        return corrected_text

    except Exception as e:
        print(f"[❌ refine_text ERROR]: {e}")
        return "Error during text refinement."


def download_default_audio(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.flac')
    tmp_file.write(response.content)
    tmp_file.close()
    return tmp_file.name

def generate_audio():
    try:
        wav = tts_model.generate(
            st.session_state.corrected_text,
            audio_prompt_path=st.session_state.ref_audio_path,
            exaggeration=st.session_state.exaggeration,
            temperature=st.session_state.temperature,
            cfg_weight=st.session_state.cfg_weight
        )
        sr = tts_model.sr
        audio_buffer = io.BytesIO()
        sf.write(audio_buffer, wav.squeeze(0).numpy(), sr, format='WAV')
        st.session_state.audio_data = audio_buffer.getvalue()
        st.success("Audio generation complete!")

    except Exception as e:
        st.error(f"Audio generation failed: {e}")


user_input = st.text_area("Enter your text:", DEFAULT_TEXT, height=150)

# --- Reference Audio Selection ---
st.subheader("🎵 Reference Audio File (Optional)")

ref_audio_option = st.radio("Select audio source:", ["Default", "Upload", "Microphone"], horizontal=True)

if ref_audio_option == "Default":
    st.audio(DEFAULT_AUDIO_URL, format="audio/flac")
    if not st.session_state.ref_audio_path or not os.path.exists(st.session_state.ref_audio_path):
        st.session_state.ref_audio_path = download_default_audio(DEFAULT_AUDIO_URL)

elif ref_audio_option == "Upload":
    uploaded_audio = st.file_uploader("Upload reference audio", type=["wav", "mp3", "flac", "m4a"])
    if uploaded_audio:
        tmp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_audio.name.split('.')[-1]}")
        tmp_audio.write(uploaded_audio.read())
        tmp_audio.close()
        st.session_state.ref_audio_path = tmp_audio.name
        st.audio(uploaded_audio)

elif ref_audio_option == "Microphone":
    st.info("🎙️ Click to record. Press stop when finished.")
    mic_audio = st_audiorec()
    if mic_audio is not None:
        tmp_mic_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        tmp_mic_file.write(mic_audio)
        tmp_mic_file.close()
        st.session_state.ref_audio_path = tmp_mic_file.name
        st.success("✅ Microphone audio saved and ready!")
    else:
        st.warning("👆 Tap 'Record', say something, then tap 'Stop'.")

tone = st.selectbox("🎨 Choose a transformation tone:", ["None (just grammar correction)"] + list(TONE_PROMPTS.keys()))

if st.button("🔧 Refine"):
    if user_input.strip():
        st.session_state.corrected_text = refine_text(user_input.strip(), tone)
        st.session_state.audio_data = None
    else:
        st.warning("Please enter some text.")

st.text_area(f"🪛 Refined Text: max 500chr ,your: {len(st.session_state.corrected_text)}chr", st.session_state.corrected_text, height=150)

# TTS Controls
st.markdown("### 🎛️ TTS Controls")
st.session_state.exaggeration = st.slider("Exaggeration", 0.25, 2.0, st.session_state.exaggeration, 0.05)
st.session_state.cfg_weight = st.slider("CFG Weight", 0.2, 1.0, st.session_state.cfg_weight, 0.05)
st.session_state.temperature = st.slider("Temperature", 0.05, 5.0, st.session_state.temperature, 0.05)

if st.button("🎧 Generate Speech"):
    generate_audio()

if st.session_state.audio_data:
    st.subheader("🔊 Generated Audio")
    st.audio(st.session_state.audio_data, format="audio/wav")
    b64_audio = base64.b64encode(st.session_state.audio_data).decode()
    st.markdown(f'<a href="data:audio/wav;base64,{b64_audio}" download="speech.wav">📥 Download Audio</a>', unsafe_allow_html=True)
