from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableSequence

from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

template = PromptTemplate(
    template="Write me a comedy joke about {topic}",
    input_variables=["topic"]
)

template2 = PromptTemplate(
    template="explain the follwoing joke -> {text} after writing actual joke in response",
    input_variables=["text"]
)

parser = StrOutputParser()

chain = RunnableSequence(
    template,
    model,
    parser,
    template2,
    model,
    parser
)

res = chain.invoke({"topic": "greedy relatives"})
print(res)