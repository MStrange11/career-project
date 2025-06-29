from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain.schema.runnable import RunnableParallel # RunnableParallel is a class that allows you to run multiple chains in parallel.

from dotenv import load_dotenv

load_dotenv()

model1 = ChatHuggingFace(llm=HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    task="text-generation",
))

model2 = ChatHuggingFace(llm=HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b-it",
    task="text-generation",
))
model3 = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

template1 = PromptTemplate(
    template="Write a short summary on the following topic. \n {text}",
    input_variables=["text"]
)
template2 = PromptTemplate(
    template="generate 5 quiz questions on the following topic. \n {text}",
    input_variables=["text"]
)
template3 = PromptTemplate(
    template="merge the summary and quiz questions into a single document. \n note -> {note} and quiz -> {quiz}",
    input_variables=["note", "quiz"]
)

parser = StrOutputParser()

parallel_chain = RunnableParallel(
    {
        "note": template1 | model1 | parser,
        "quiz": template2 | model2 | parser
    }
)

merge_chain = template3 | model3 | parser

chain = parallel_chain | merge_chain

chain.get_graph().print_ascii()

text = '''
Simple and compound interest are two ways to calculate interest on a principal amount. Simple interest is calculated only on the principal, while compound interest is calculated on the principal and accumulated interest from previous periods. This leads to different growth patterns: simple interest grows linearly, while compound interest grows exponentially. 
Simple Interest:
Calculated only on the original principal amount. 
Interest earned or paid remains constant over time. 
Formula: SI = (P * R * T) / 100 where SI is simple interest, P is the principal, R is the interest rate, and T is the time period. 
Compound Interest:
Calculated on the principal amount and the accumulated interest from previous periods. 
Interest earned or paid increases over time as the principal grows. 
Formula: A = P (1 + R/n)^(nt) where A is the amount after t years, P is the principal, R is the annual interest rate, n is the number of times interest is compounded per year, and t is the number of years. 
'''

res = chain.invoke({"text": text})
print(res) 