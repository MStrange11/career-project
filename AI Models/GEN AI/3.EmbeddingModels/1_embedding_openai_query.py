from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

emb = OpenAIEmbeddings(
    model="text-embedding-3-small",
    dimensions=32
)

'''
What is dimensions?
Dimensions refer to the size of the embedding vector that the model will return. For example, if you set dimensions=32, the output will be a vector with 32 floating-point numbers representing the embedding of the input text.

What this means is that the model will convert the input text into a numerical representation that captures its semantic meaning, and this representation will be a vector of 32 numbers.

use for cosine similarity or other vector operations.
'''

try:
    res = emb.embed_query('What is the capital of France?')
except Exception as e:
    if "429" in str(e):
        res = "Rate limit exceeded. Please try again later. Upgrading your plan."
        res += "\nexample output: [0.123456, -0.234567, ...] with length of 32 as given in dimensions=32"
    else:
        res = str(e)

print(res)
# Output: [0.123456, -0.234567, ...] (example output)

'''
What is the maximum length of the embedding vector?
The maximum length of the embedding vector will be 1536 for the small model and 3072 for the large model.
'''