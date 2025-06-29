from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableSequence, RunnableParallel

from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

template = PromptTemplate(
    template="Generate tweet about {topic}",
    input_variables=["topic"]
)

template2 = PromptTemplate(
    template="Generate linkedin post about {topic}",
    input_variables=["topic"]
)

parser = StrOutputParser()

# RunnableParallel is a class that allows you to run multiple chains in parallel. it return a dict output
parallel_chain = RunnableParallel(
    {
        "tweet": RunnableSequence(
            template,
            model,
            parser
        ),
        "linkedin": RunnableSequence(
            template2,
            model,
            parser
        )
    }
)

res = parallel_chain.invoke({"topic": "python developer job"})
for key, value in res.items():
    print(f"{key}: {value}\n\n")

