from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# 1. Define tools
@tool
def conversion_factor(base_currency: str, target_currency: str) -> float:
    """This function fetches the currency conversion factor between a given base currency and a target currency."""
    data = requests.get(
        f"https://v6.exchangerate-api.com/v6/{os.getenv('EXCHANGE_RATE_API_KEY')}/pair/{base_currency}/{target_currency}"
    ).json()
    return data["conversion_rate"]  # Return only the float

@tool
def convert(base_currency_value: float, conversion_rate: float) -> float:
    """Given a currency conversion rate, calculates the target currency value."""
    return base_currency_value * conversion_rate

# 2. Bind LLM with tools
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
llm_with_tools = llm.bind_tools([conversion_factor, convert])

# 3. Start conversation
messages = [HumanMessage(content="What is the conversion factor between INR and USD, and based on that can you convert 10 USD to INR?")]

# 4. LLM makes tool call(s)
ai_response = llm_with_tools.invoke(messages)
messages.append(ai_response)

# 5. Process tool calls
tool_outputs = []

for tool_call in ai_response.tool_calls:
    if tool_call["name"] == "conversion_factor":
        result = conversion_factor.invoke(tool_call["args"])
        messages.append(ToolMessage(tool_call_id=tool_call["id"], content=str(result)))
        conversion_rate = result  # Save for next call
    elif tool_call["name"] == "convert":
        tool_call["args"]["conversion_rate"] = conversion_rate  # Inject manually
        result = convert.invoke(tool_call["args"])
        messages.append(ToolMessage(tool_call_id=tool_call["id"], content=str(result)))

ai_response = llm_with_tools.invoke(messages)
messages.append(ai_response)

for tool_call in ai_response.tool_calls:
    if tool_call["name"] == "conversion_factor":
        result = conversion_factor.invoke(tool_call["args"])
        messages.append(ToolMessage(tool_call_id=tool_call["id"], content=str(result)))
        conversion_rate = result  # Save for next call
    elif tool_call["name"] == "convert":
        tool_call["args"]["conversion_rate"] = conversion_rate  # Inject manually
        result = convert.invoke(tool_call["args"])  
        messages.append(ToolMessage(tool_call_id=tool_call["id"], content=str(result)))

ai_response = llm_with_tools.invoke(messages)
messages.append(ai_response)

for m in messages:
    print(m, "\n")

print(messages[-1].content)
