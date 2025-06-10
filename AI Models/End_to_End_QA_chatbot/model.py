import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()  # Load .env file
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# List models
models = genai.list_models()
print("Available models:")
for model in models:
    print(model.name)
