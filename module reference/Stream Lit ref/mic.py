import streamlit as st
import base64
import io
from datetime import datetime
import os

# Set page config
st.set_page_config(
    page_title="Voice Recorder",
    page_icon="🎙️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    
    .recording-container {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        border: 2px solid #e9ecef;
    }
    
    .audio-container {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #28a745;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .status-message {
        padding: 0.5rem;
        border-radius: 5px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
    }
    
    .success {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .info {
        background-color: #d1ecf1;
        color: #0c5460;
        border: 1px solid #bee5eb;
    }
    
    .recording-indicator {
        color: #dc3545;
        font-size: 1.2em;
        animation: blink 1s infinite;
    }
    
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0.3; }
    }
    
    audio {
        width: 100%;
        margin: 1rem 0;
    }
    
    .download-section {
        margin-top: 2rem;
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 8px;
        border-left: 4px solid #17a2b8;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'recordings' not in st.session_state:
    st.session_state.recordings = []
if 'current_recording' not in st.session_state:
    st.session_state.current_recording = None

# App header
st.markdown('<h1 class="main-header">🎙️ Voice Recorder</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; margin-bottom: 2rem;">Record your voice directly in the browser with full playback controls</p>', unsafe_allow_html=True)

# Try to import and use streamlit_audio_recorder
try:
    from streamlit_audio_recorder import st_audiorec
    
    # Recording section
    st.markdown('<div class="recording-container">', unsafe_allow_html=True)
    st.subheader("🎤 Record Audio")
    
    # Audio recorder component
    wav_audio_data = st_audiorec()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle recorded audio
    if wav_audio_data is not None:
        # Store the current recording
        st.session_state.current_recording = wav_audio_data
        
        # Add to recordings list with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        recording_entry = {
            'data': wav_audio_data,
            'timestamp': timestamp,
            'id': len(st.session_state.recordings)
        }
        
        # Check if this is a new recording (avoid duplicates)
        if not st.session_state.recordings or recording_entry['data'] != st.session_state.recordings[-1]['data']:
            st.session_state.recordings.append(recording_entry)
        
        # Success message
        st.markdown('<div class="status-message success">✅ Recording completed successfully!</div>', unsafe_allow_html=True)
        
        # Audio playback section
        st.markdown('<div class="audio-container">', unsafe_allow_html=True)
        st.subheader("🔊 Playback")
        
        # Display audio player with full controls
        st.audio(wav_audio_data, format='audio/wav', start_time=0)
        
        # Audio information
        audio_size = len(wav_audio_data)
        st.info(f"📊 **Recording Info:**\n- Size: {audio_size:,} bytes ({audio_size/1024:.1f} KB)\n- Format: WAV\n- Recorded: {timestamp}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download section
        st.markdown('<div class="download-section">', unsafe_allow_html=True)
        st.subheader("💾 Download Recording")
        
        # Create download filename
        filename = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        
        # Download button
        st.download_button(
            label="⬇️ Download Audio File",
            data=wav_audio_data,
            file_name=filename,
            mime="audio/wav",
            help="Download the recorded audio as a WAV file"
        )
        st.markdown('</div>', unsafe_allow_html=True)

except ImportError:
    # Fallback UI if streamlit_audio_recorder is not available
    st.error("📦 **Installation Required**")
    st.markdown("""
    To use this voice recorder app, you need to install the required package:
    
    ```bash
    pip install streamlit-audio-recorder
    ```
    
    Then restart your Streamlit app.
    """)
    
    # Show demo interface
    st.markdown('<div class="recording-container">', unsafe_allow_html=True)
    st.subheader("🎤 Voice Recorder Interface")
    st.info("This is a preview of the interface. Install the required package to enable recording functionality.")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎙️ Start Recording", disabled=True):
            pass
        if st.button("⏹️ Stop Recording", disabled=True):
            pass
    
    st.markdown('</div>', unsafe_allow_html=True)

# Recording history section
if st.session_state.recordings:
    st.markdown("---")
    st.subheader("📚 Recording History")
    
    for i, recording in enumerate(reversed(st.session_state.recordings)):
        with st.expander(f"🎵 Recording #{len(st.session_state.recordings) - i} - {recording['timestamp']}"):
            st.audio(recording['data'], format='audio/wav')
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"Size: {len(recording['data']):,} bytes")
            with col2:
                filename = f"recording_{recording['timestamp'].replace(':', '').replace('-', '').replace(' ', '_')}.wav"
                st.download_button(
                    label="⬇️ Download",
                    data=recording['data'],
                    file_name=filename,
                    mime="audio/wav",
                    key=f"download_{recording['id']}"
                )

# Instructions
st.markdown("---")
st.markdown("""
### 📋 Instructions

1. **Click the microphone button** to start recording
2. **Speak into your microphone** - the recording will begin automatically
3. **Click the stop button** to end the recording
4. **Use the audio player** to listen to your recording with full controls:
   - Play/Pause button
   - Volume control
   - Seek bar for navigation
   - Playback speed control (browser dependent)
5. **Download your recording** as a WAV file using the download button

### 🔧 Technical Requirements

- Modern web browser with microphone support
- Microphone permissions granted to the browser
- `streamlit-audio-recorder` package installed

### 🔒 Privacy & Security

- All recordings are processed locally in your browser
- No audio data is sent to external servers
- Recordings are stored temporarily in your browser session
""")

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #888; font-size: 0.8em;">Built with Streamlit 🚀</p>',
    unsafe_allow_html=True
)