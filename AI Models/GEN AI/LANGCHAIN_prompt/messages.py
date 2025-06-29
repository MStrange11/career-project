from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
load_dotenv()

# Initialize the Google Generative AI model
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="tell me about langchain"),
]

response = model.invoke(messages)

messages.append(AIMessage(content=response.content))

print(messages)