from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage # you can remove this line
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
load_dotenv()

# Initialize the Google Generative AI model
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Define a chat prompt template
chat_template = ChatPromptTemplate([
    SystemMessage(content="You are a helpful {domain} expert."),
    HumanMessage(content="Explain in simple terms what {topic} is."),
]) # not muture way to use ChatPromptTemplate, because the dynemic variables are not supported in the messages directly.

chat_template = ChatPromptTemplate([
    ('system', "You are a helpful {domain} expert."),
    ('human', "Explain in simple terms what {topic} is."),
])


prompt = chat_template.invoke({
    "domain": "Python programming",
    "topic": "decorators"
})

print(prompt, "\n------------\n")

# res = model.invoke(prompt)
# print(res.content)