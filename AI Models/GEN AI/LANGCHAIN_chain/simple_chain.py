from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

template = PromptTemplate(
    template="Write a 5 point summary on the following topic. \n {text}",
    input_variables=["text"]
)

chain = template | ChatGoogleGenerativeAI(model="gemini-1.5-flash") | StrOutputParser()

chain.get_graph().print_ascii()

res = chain.invoke({"text": "Shinchan cartoon"})
print(res)
