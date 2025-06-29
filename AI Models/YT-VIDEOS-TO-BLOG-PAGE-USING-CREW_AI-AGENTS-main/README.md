# YouTube Blog Generator using CrewAI

This project uses **CrewAI** to build a smart system that:

1. **Searches YouTube videos from a specific channel** (e.g., Krishnaik’s channel)
2. **Extracts relevant video information** based on a given topic
3. **Generates a blog post** summarizing that information


##  What It Does

* Uses two AI agents:

  * **Blog Researcher**: Finds the most relevant YouTube video and extracts detailed information.
  * **Blog Writer**: Converts the extracted data into a readable, engaging blog post.

* Automatically saves the final blog content to a file: `new-blog-post.md`.


## Setup Instructions

### 1. Install Required Packages

```cmd
pip install -r requirements.txt
```

### 2. Add your API key in a `.env` file

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key
```

## How to Run

Run the following script:

```cmd
python crew.py
```

The AI agents will:

1. Search Krishnaik’s channel for videos related to the topic.
2. Extract useful insights.
3. Write a blog post.
4. Save the blog to `new-blog-post.md`.

## Example

Input topic:

```text
AI VS ML VS DL vs Data Science
```

Output file: `new-blog-post.md` (Contains a blog explaining this topic in simple language)

## Channel Used

This system searches videos from:

* [Krishnaik's YouTube Channel](https://www.youtube.com/@krishnaik06)

## Notes

* You can change the topic in `crew.py` (`inputs={'topic': 'your_topic_here'}`).
* You can change the channel by updating the handle in `tools.py`.
