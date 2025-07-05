from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

from dotenv import load_dotenv
load_dotenv()

@tool
def multiply(a: int, b: int) -> int:
    '''given 2 number a and b this retrun their product'''
    print("multiply function called")
    return a * b

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
llm_withTools = llm.bind_tools([multiply])

query_message = "can you multiply 20 and 11?"
messages = [HumanMessage(content=query_message)]

res = llm_withTools.invoke(messages)
messages.append(res)

messages.append(multiply.invoke(res.tool_calls[0]))

res = llm_withTools.invoke(messages)
print(res.content)