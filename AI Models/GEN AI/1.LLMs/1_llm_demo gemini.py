from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.2)

res = llm.invoke("Create a presentation points on the topic 'Artificial Intelligence in AR and VR'.")

print(res.content)
# Output: 'The capital of France is Paris.'