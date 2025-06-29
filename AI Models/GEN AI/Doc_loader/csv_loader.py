from langchain_community.document_loaders import CSVLoader

loader = CSVLoader("Doc_loader/Social_Network_Ads.csv")
docs = loader.load()
print("Number of rows:",len(docs))

print("page_content:",docs[0].page_content.replace("\n", " | "))
print("metadata:",docs[0].metadata)
