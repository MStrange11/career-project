from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableBranch ,RunnableSequence, RunnablePassthrough

from dotenv import load_dotenv
load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

prompt1 = PromptTemplate(
    template="Write a new report about the following topic \n {topic}",
    input_variables=["topic"]
)

prompt2 = PromptTemplate(
    template="Summarize the following text under 300 words \n {text}",
    input_variables=["text"]
)



parser = StrOutputParser()

# chain = RunnableSequence(prompt1,model,parser,
#     RunnableBranch(
#         (lambda x:len(x.split()) > 300, RunnableSequence(prompt2, model, parser)),
#         RunnablePassthrough()
#     )
# )
chain = prompt1 | model | parser

res = chain.invoke({"topic": "Battleground PUBG"})
print(res)