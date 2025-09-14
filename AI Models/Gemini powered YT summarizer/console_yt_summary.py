import os
import re
import json
from pathlib import Path
from datetime import datetime
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

class YouTubeSummarizer:
    def __init__(self):
        # Initialize models
        self.embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)
        
        # Constants
        self.DB_DIR = "LANGCHAIN_rag"
        self.DB_PATH = os.path.join(self.DB_DIR, "faiss_db")
        self.VIDEO_METADATA_PATH = os.path.join(self.DB_DIR, "video_metadata.json")
        
        # Ensure directories exist
        Path(self.DB_DIR).mkdir(parents=True, exist_ok=True)
        
        # Initialize variables
        self.video_id = None
        self.vector_store = None
        self.summary = None

    def get_video_id(self, url):
        """Extract video ID from YouTube URL"""
        youtube_regex = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        )
        
        match = re.search(youtube_regex, url)
        if match:
            return match.group(6)
        return None

    def save_video_metadata(self, **data):
        """Save video metadata for future reference"""
        metadata = {
            "video_id": data.get("video_id"),
            "url": data.get("url"),
            "summery": "",
            "questions": "",
            "answers": ""
        }
        
        if os.path.exists(self.VIDEO_METADATA_PATH):
            with open(self.VIDEO_METADATA_PATH, 'r') as f:
                existing_data = json.load(f)
            
            for k, v in data.items():
                existing_data[k] = v
        else:
            existing_data = metadata
            for k, v in data.items():
                existing_data[k] = v
        
        with open(self.VIDEO_METADATA_PATH, 'w') as f:
            json.dump(existing_data, f, indent=4)

    def load_last_video_metadata(self):
        """Load video metadata for future reference"""
        if os.path.exists(self.VIDEO_METADATA_PATH):
            with open(self.VIDEO_METADATA_PATH, 'r') as f:
                try:
                    return json.load(f)
                except Exception:
                    pass
        return {}

    def indexing(self, video_id, url):
        """Index YouTube video transcript"""
        try:
            print("📥 Fetching video transcript...")
            # Updated API usage
            ytt_api = YouTubeTranscriptApi()
            transcript = ytt_api.fetch(video_id, languages=["en"])
            
            # Convert to text format
            transcript_text = " ".join([snippet.text for snippet in transcript])
            
            print("✂️  Splitting text into chunks...")
            # text splitter
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.create_documents([transcript_text])
            
            print("🔤 Creating embeddings...")
            # embedding
            vector_store = FAISS.from_documents(chunks, self.embedding_model)
            
            print("💾 Saving vector store...")
            # save vector store
            vector_store.save_local(self.DB_PATH)
            
            # save video metadata
            self.save_video_metadata(video_id=video_id, url=url)
            
            return vector_store
        except TranscriptsDisabled:
            print("❌ Error: Transcript is disabled for this video")
            return None
        except VideoUnavailable:
            print("❌ Error: Video is unavailable or doesn't exist")
            return None
        except Exception as e:
            print(f"❌ An error occurred: {str(e)}")
            return None

    def load_vector_store(self):
        """Load existing vector store if available"""
        try:
            if os.path.exists(self.DB_PATH):
                return FAISS.load_local(self.DB_PATH, self.embedding_model, allow_dangerous_deserialization=True)
            return None
        except Exception as e:
            print(f"❌ Error loading vector store: {str(e)}")
            return None

    def get_summary_or_answer(self, vector_store, question):
        """Generate summary or answer from vector store"""
        prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="You are a helpful assistant. Answer the question based on the given context.\n\nContext: {context}\n\nQuestion: {question}"
        )

        chain = RunnableParallel(
            {
                "context": vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4}) | RunnableLambda(lambda r: "\n\n".join([doc.page_content for doc in r])),
                "question": RunnablePassthrough()
            }
        ) | prompt_template | self.llm | StrOutputParser()

        return chain.invoke(question)

    def process_video(self, youtube_url):
        """Process a YouTube video"""
        print(f"🔗 Processing URL: {youtube_url}")
        
        video_id = self.get_video_id(youtube_url)
        if not video_id:
            print("❌ Invalid YouTube URL. Please enter a valid YouTube URL.")
            return False
        
        self.video_id = video_id
        print(f"🎬 Video ID: {video_id}")
        
        # Index the video
        self.vector_store = self.indexing(video_id, youtube_url)
        
        if self.vector_store:
            print("✅ Video processed successfully!")
            return True
        else:
            print("❌ Failed to process video.")
            return False

    def generate_summary(self):
        """Generate and display video summary"""
        if not self.vector_store:
            print("❌ No video loaded. Please process a video first.")
            return
        
        print("\n📝 Generating video summary...")
        self.summary = self.get_summary_or_answer(self.vector_store, "Please provide a comprehensive summary of the video transcript, highlighting the main topics, key points, and important information discussed.")
        self.save_video_metadata(summery=self.summary)
        
        print("\n" + "="*80)
        print("📋 VIDEO SUMMARY:")
        print("="*80)
        print(self.summary)
        print("="*80)

    def start_conversation(self):
        """Start interactive Q&A session"""
        if not self.vector_store:
            print("❌ No video loaded. Please process a video first.")
            return
        
        print("\n💬 Starting Q&A session...")
        print("You can now ask questions about the video. Type 'quit' or 'exit' to end the session.")
        print("-" * 80)
        
        while True:
            question = input("\n❓ Your question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye! Thanks for using YouTube Summarizer.")
                break
            
            if not question:
                print("Please enter a question or type 'quit' to exit.")
                continue
            
            print("\n🤔 Thinking...")
            answer = self.get_summary_or_answer(self.vector_store, question)
            self.save_video_metadata(questions=question, answers=answer)
            
            print("\n" + "="*80)
            print("💡 ANSWER:")
            print("="*80)
            print(answer)
            print("="*80)

    def run(self):
        """Main application loop"""
        print("🎥 YouTube Video Summarizer - Console Version")
        print("=" * 50)
        
        # Check if there's a previous session
        metadata = self.load_last_video_metadata()
        if metadata.get("video_id"):
            print(f"📁 Found previous session with video ID: {metadata.get('video_id')}")
            print(f"🔗 URL: {metadata.get('url', 'Unknown')}")
            
            load_previous = input("Load previous session? (y/n): ").strip().lower()
            if load_previous == 'y':
                self.vector_store = self.load_vector_store()
                if self.vector_store:
                    self.video_id = metadata.get("video_id")
                    print("✅ Previous session loaded successfully!")
                    
                    # Show previous summary if available
                    if metadata.get("summery"):
                        print("\n📋 Previous Summary:")
                        print("-" * 80)
                        print(metadata.get("summery"))
                        print("-" * 80)
                    
                    # Start conversation
                    self.start_conversation()
                    return
                else:
                    print("❌ Could not load previous session.")
        
        # Get YouTube URL from user
        while True:
            youtube_url = input("\n🔗 Enter YouTube URL: ").strip()
            
            if not youtube_url:
                print("Please enter a YouTube URL.")
                continue
            
            if youtube_url.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                return
            
            # Process the video
            if self.process_video(youtube_url):
                break
            else:
                retry = input("Would you like to try another URL? (y/n): ").strip().lower()
                if retry != 'y':
                    return
        
        # Generate summary
        self.generate_summary()
        
        # Start conversation
        self.start_conversation()


def main():
    """Entry point"""
    try:
        summarizer = YouTubeSummarizer()
        summarizer.run()
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()