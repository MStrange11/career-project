from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableSequence, RunnablePassthrough, RunnableParallel, RunnableLambda

from dotenv import load_dotenv
load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

template = PromptTemplate(
    template="Write me a comedy joke about {topic}",
    input_variables=["topic"]
)

parser = StrOutputParser()

chain = RunnableSequence(
    template,
    model,
    parser,
    RunnableParallel({
        "joke": RunnablePassthrough(),
        "word_count": RunnableLambda(lambda x: len(x.split(" ")))
    })
)

res = chain.invoke({"topic": "new python programmar"})
print("Joke: ",res['joke'])
print()
print("Word Count: ",res['word_count'])
