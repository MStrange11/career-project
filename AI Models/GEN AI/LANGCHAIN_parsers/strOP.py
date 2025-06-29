# StrOutputParsers

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser


load_dotenv()


llm = HuggingFaceEndpoint(
    # repo_id='mistralai/Mistral-7B-Instruct-v0.3',
    repo_id='google/gemma-2-2b-it',
    task='text2text-generation',
)

model = ChatHuggingFace(llm=llm)


template1 = PromptTemplate(
    template='Write a detailed report on {topic}',
    input_variables=['topic']
)

template2 = PromptTemplate(
    template='write a 5 line summary  on the following text. \n {text}',
    input_variables=['text']
)

prompt1 = template1.invoke({'topic':'black holes'})

res1 = model.invoke(prompt1)

prompt2 = template2.invoke({'text':res1.content})

res2 = model.invoke(prompt2)

# print(f"Report on black holes: {res1.content}")
# print("\n"*5)
# print(f"Summary of the report: {res2.content}")

parser = StrOutputParser()

chain = template1 | model | parser | template2 | model | parser

res = chain.invoke({'topic': 'black holes'})
print(f"Report on black holes: {res}")