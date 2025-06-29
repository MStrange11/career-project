from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://en.wikipedia.org/wiki/Architecture")

docs = loader.load()
# print(len(docs[0].page_content))
# print(docs[0])

# lets ask question on this web content from LLM

if 1:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import StrOutputParser

    from dotenv import load_dotenv
    load_dotenv()
    
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

    template = PromptTemplate(
        template="Answer the question based on the following context \n {context} \n Question: {question}",
        input_variables=["context", "question"]
    )

    chain = template | model | StrOutputParser()
    
    res = chain.invoke({"context": docs[0].page_content, "question": "What is architecture?"})
    print(res)