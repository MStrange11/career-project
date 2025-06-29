from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

template = PromptTemplate(
    template="Generate a detail report on {topic}",
    input_variables=["topic"]
)

template2 = PromptTemplate(
    template="Generate a 5 pointer summary on the following text. \n {text}",
    input_variables=["text"]
)

parser = StrOutputParser()

chain = template | model | parser | template2 | model | parser

chain.get_graph().print_ascii()

res = chain.invoke({"topic": "Doremon movie steel troops"})
print(res)
