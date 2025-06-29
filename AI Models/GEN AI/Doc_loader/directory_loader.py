from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

loader = DirectoryLoader("Doc_loader/Books",
    glob="*.pdf", 
    loader_cls=PyPDFLoader)


docs = loader.load()
print(len(docs))
print(docs[0])
