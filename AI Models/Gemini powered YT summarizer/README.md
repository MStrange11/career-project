# YouTube Transcript to Summary App

This app is a user-friendly tool built with Streamlit that allows you to quickly get summarized notes from any YouTube video that has a transcript available.

### How It Works

1. **Input YouTube Video Link:**
   You enter the link of the YouTube video you want to summarize.

2. **Transcript Extraction:**
   The app extracts the video's transcript automatically using the `youtube-transcript-api`. This step fetches the spoken text from the video if captions or subtitles are available.

3. **Video Thumbnail Display:**
   It shows the thumbnail image of the video to confirm the correct video is being processed.

4. **AI-Powered Summarization:**
   The extracted transcript is sent to Google’s Gemini 1.5 Pro model, a powerful language model that reads through the text and generates a concise summary in easy-to-understand points within 250 words.

5. **Display Summary:**
   The app then displays this summarized content as detailed notes, helping you grasp the main ideas and key points quickly without watching the entire video.

### Key Features

* Supports most YouTube videos with transcripts.
* Handles different types of videos — educational, storytelling, tutorials, and more.
* Provides clear error messages when transcripts are unavailable or videos are invalid.
* Simple and clean interface for easy use.

### Why Use This App?

Watching full-length videos can be time-consuming. This app helps save your time by extracting meaningful summaries, allowing you to learn or review content quickly. It’s especially useful for students, researchers, or anyone who frequently consumes YouTube educational content.

## How to Run the App

### Prerequisites

Make sure you have Python installed on your system (Python 3.7 or higher recommended).

### Use the app

* Paste a YouTube video link in the input box.
* Click the button to generate a summary.
* View the summarized notes on the page.

