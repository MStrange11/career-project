from langchain_huggingface import ChatHuggingFace,HuggingFacePipeline
from dotenv import load_dotenv
load_dotenv()

import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

llm = HuggingFacePipeline.from_model_id(
    model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0", # this model is no more free to use
    task="text-generation",
    pipeline_kwargs={"temperature": 0.7, "max_new_tokens": 512},
)

model = ChatHuggingFace(llm=llm)

try:
    res = model.invoke("what is the capital of India?").content
except Exception as e:
    res = str(e) 

print(res)