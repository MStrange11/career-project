# https://platform.openai.com/settings/organization/billing/overview


from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()


model = ChatOpenAI(model = "gpt-4o", temperature=0, max_completion_tokens=1000)

'''
What is temperature?
Temperature is a parameter that controls the randomness of the model's responses. 
A lower temperature (e.g., 0.0) makes the model more deterministic and focused, 
while a higher temperature (e.g., 1.0) allows for more creative and varied responses (like storytelling).


What is max_completion_tokens?
max_completion_tokens is a parameter that limits the number of tokens (words or word pieces) in the model's response.
This helps control the length of the output, ensuring it doesn't exceed a certain size.
'''


try:
    res = model.invoke("What is the capital of France?")
except Exception as e:
    if "429" in str(e):
        res = "You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com"
    else:
        res = str(e)

print(res)

'''
Output: A json object with the response from the model, 
json['content'].

more data (metadata) can be found in the json object, such as
- model version
- response time
- token usage
- etc.

'''