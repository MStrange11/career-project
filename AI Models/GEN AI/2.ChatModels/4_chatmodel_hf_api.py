from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv  
load_dotenv()

# repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
repo_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  

llm = HuggingFaceEndpoint(
    repo_id = repo_id,
    task = "text-generation",
)

model = ChatHuggingFace(llm=llm)

try:
    res = model.invoke("what is the capital of India?").content
except Exception as e:
    if "StopIteration" == str(e.__class__.__name__):
        res = "The model did not return a response. Model has no Inference Providers configured."
    else:
        res = str(e)

print(res)