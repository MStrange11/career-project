from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import json

load_dotenv()

# emb = OpenAIEmbeddings(
#     model="text-embedding-3-small",
#     dimensions=32
# )

emb = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    dimensions=32
)

documentation = [
    'Delhi is the capital of India.',
    'Paris is the capital of France.',
    'Berlin is the capital of Germany.',
    'Tokyo is the capital of Japan.',
    'Canberra is the capital of Australia.'
]


try:
    res = emb.embed_documents(documentation)
except Exception as e:
    if "429" in str(e):
        res = "Rate limit exceeded. Please try again later. Upgrading your plan."
        res += "\nexample output: [[0.123456, -0.234567, ... upto 32 index],[0.125848,0.855662,... upto 32],... len(documentation)] with length of 32 as given in dimensions=32"
    else:
        res = str(e)

print(json.dumps({"shape":f"{len(res)}x{len(res[0])}", "first line":res[0][:5]}, indent=4))
# Output: [[0.123456, -0.234567, ... upto 32 index],[0.125848,0.855662,... upto 32],...] (example output)
