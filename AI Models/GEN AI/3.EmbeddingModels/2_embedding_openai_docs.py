from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

emb = OpenAIEmbeddings(
    model="text-embedding-3-small",
    dimensions=32
)

documentation = [
    'Delhi is the capital of India.',
    'Paris is the capital of France.',
    'Berlin is the capital of Germany.',
    'Tokyo is the capital of Japan.',
    'Canberra is the capital of Australia.',
    'Ottawa is the capital of Canada.',
    'Moscow is the capital of Russia.',
    'Beijing is the capital of China.',
    'Brasília is the capital of Brazil.',
    'Rome is the capital of Italy.',
    'Madrid is the capital of Spain.',
    'Addis Ababa is the capital of Africa.',
    'London is the capital of the United Kingdom.',
]


try:
    res = emb.embed_documents(documentation)
except Exception as e:
    if "429" in str(e):
        res = "Rate limit exceeded. Please try again later. Upgrading your plan."
        res += "\nexample output: [[0.123456, -0.234567, ... upto 32 index],[0.125848,0.855662,... upto 32],... len(documentation)] with length of 32 as given in dimensions=32"
    else:
        res = str(e)

print(res)
# Output: [[0.123456, -0.234567, ... upto 32 index],[0.125848,0.855662,... upto 32],...] (example output)
