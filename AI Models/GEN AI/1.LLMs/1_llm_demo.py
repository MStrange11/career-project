from langchain_openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(model= "gpt-3.5-turbo-instruct")

res = llm.invoke("What is the capital of France?")

print(res)
# Output: 'The capital of France is Paris.'