# 📝 Grammar Refiner + 🎤 Text-to-Speech (TTS) Generator

This project is a **Streamlit web app** that combines:\
- **Grammar correction & tone transformation** powered by **Google
Gemini 1.5 Flash**\
- **Voice cloning & speech generation** powered by **Chatterbox TTS**

It allows users to enter text, refine it into various tones, and
generate natural-sounding speech from a reference voice (default,
uploaded, or recorded).

### Project origin (https://github.com/MStrange11/AI-voice-tuner)

------------------------------------------------------------------------

## 🚀 Features

-   ✅ **Grammar Correction** -- Automatically fixes grammar and
    spelling.\
-   🎨 **Tone Transformation** -- 18 tone options (formal, poetic,
    sarcastic, academic, etc.).\
-   🎤 **Voice Options** -- Use a default sample, upload your own, or
    record with a microphone.\
-   🎛️ **Customizable Speech Controls** -- Exaggeration, CFG Weight, and
    Temperature.\
-   🔊 **High-Quality TTS** -- Generate realistic speech from refined
    text.\
-   📥 **Download Option** -- Save generated speech as a `.wav` file.

------------------------------------------------------------------------

## 📦 Installation

### 1️⃣ Clone the Repository

``` bash
git clone https://github.com/your-username/grammar-refiner-tts.git
cd grammar-refiner-tts
```

### 2️⃣ Create a Virtual Environment

``` bash
# Windows
py -3.10 -m venv Myenv
Myenv\Scripts\activate

# macOS/Linux
python3.10 -m venv Myenv
source Myenv/bin/activate
```

### 3️⃣ Install Dependencies

``` bash
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables

Create a `.env` file in the project root with your Google API key:

``` ini
GOOGLE_API_KEY=your_google_api_key_here
```

> ⚠️ You must have access to [Google Gemini
> API](https://ai.google.dev/).

------------------------------------------------------------------------

## ▶️ Usage

Run the app with Streamlit:

``` bash
streamlit run app.py
```

Open your browser at **http://localhost:8501**

------------------------------------------------------------------------

## 🛠️ Workflow

1.  **Enter Text** -- Paste or type the base text.\
2.  **Refine** -- Correct grammar and optionally change tone.\
3.  **Select Voice Reference** -- Choose between:
    -   Default sample\
    -   Upload audio (`.wav`, `.mp3`, `.flac`, `.m4a`)\
    -   Record with microphone\
4.  **Adjust TTS Controls** --
    -   **Exaggeration** → controls emotional emphasis\
    -   **CFG Weight** → controls adherence to reference audio\
    -   **Temperature** → controls randomness/creativity\
5.  **Generate Speech** -- Listen, download, or regenerate as needed.

------------------------------------------------------------------------

## 📖 Use Cases

-   🗣 **Public Speaking Practice** -- Improve speech delivery.\
-   ✍️ **Content Creation** -- Blogs, stories, or scripts with different
    tones.\
-   📢 **Voice-over Generation** -- Narrations, ads, or presentations.\
-   🎮 **Game Development** -- Generate NPC dialogue in multiple
    styles.\
-   🎓 **Education** -- Simplify complex text or create academic
    material.

------------------------------------------------------------------------

## ⚡ Tech Stack

-   **Frontend/UI:** Streamlit\
-   **LLM Engine:** Google Gemini 1.5 Flash\
-   **TTS Engine:** Chatterbox\
-   **ML Framework:** PyTorch\
-   **Audio Handling:** Soundfile, torchaudio, librosa

------------------------------------------------------------------------

## 📌 Requirements

Dependencies are listed in [`requirements.txt`](requirements.txt).

Main libraries include:\
- `streamlit`\
- `torch`, `torchaudio`\
- `soundfile`, `librosa`\
- `google-generativeai`\
- `Chatterbox`\
- `streamlit-audio-recorder`\
- `python-dotenv`

------------------------------------------------------------------------

## 🧑‍💻 Contributing

Pull requests are welcome! If you'd like to add new tone styles, TTS
improvements, or UI features:

1.  Fork the repo\
2.  Create a feature branch\
3.  Commit changes\
4.  Open a PR

------------------------------------------------------------------------

## 📜 License

This project is licensed under the **MIT License**.
