from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("Doc_loader\dl-curriculum.pdf")
docs = loader.load()
print("Number of pages:",len(docs),"\n\n",type(docs[0]), "\n\n",docs[0])

print("\n\nFirst page content:  ",docs[0].page_content)
print("\n\nSecond page content:  ",docs[1].page_content)
print("\n\nLast page content:  ",docs[-1].page_content)