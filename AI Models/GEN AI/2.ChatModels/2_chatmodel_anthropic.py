# https://www.anthropic.com/api

from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
load_dotenv()

model = ChatAnthropic(model="claude-2", temperature=0, max_completion_tokens=1000)
try:
    res = model.invoke("What is the capital of France?")    
except Exception as e:
    pass

print(res)