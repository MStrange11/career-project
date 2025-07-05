import google.generativeai as genai
import dotenv
dotenv.load_dotenv()

genai.configure(api_key=key) 

for model in genai.list_models():
    if "embedding" in model.name:
        print(model.name)