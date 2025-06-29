from langchain_community.document_loaders import TextLoader

loader = TextLoader("Doc_loader/text.txt", encoding="utf-8")
docs = loader.load()
print(docs)


# we get the text file content, now from docs[0].page_content we will get file text
print(docs[0].page_content)

# for now we can send this text to LLM to do task like: summary, question answer, etc