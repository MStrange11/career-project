# !pip install langchain chromadb openai tiktoken pypdf langchain_openai langchain-community

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document

from dotenv import load_dotenv
load_dotenv()

# Create LangChain documents for IPL players

doc1 = Document(
        page_content="Virat Kohli is one of the most successful and consistent batsmen in IPL history. Known for his aggressive batting style and fitness, he has led the Royal Challengers Bangalore in multiple seasons.",
        metadata={"team": "Royal Challengers Bangalore"}
    )
doc2 = Document(
        page_content="Rohit Sharma is the most successful captain in IPL history, leading Mumbai Indians to five titles. He's known for his calm demeanor and ability to play big innings under pressure.",
        metadata={"team": "Mumbai Indians"}
    )
doc3 = Document(
        page_content="MS Dhoni, famously known as Captain Cool, has led Chennai Super Kings to multiple IPL titles. His finishing skills, wicketkeeping, and leadership are legendary.",
        metadata={"team": "Chennai Super Kings"}
    )
doc4 = Document(
        page_content="Jasprit Bumrah is considered one of the best fast bowlers in T20 cricket. Playing for Mumbai Indians, he is known for his yorkers and death-over expertise.",
        metadata={"team": "Mumbai Indians"}
    )
doc5 = Document(
        page_content="Ravindra Jadeja is a dynamic all-rounder who contributes with both bat and ball. Representing Chennai Super Kings, his quick fielding and match-winning performances make him a key player.",
        metadata={"team": "Chennai Super Kings"}
    )

docs = [doc1, doc2, doc3, doc4, doc5]

vector_store = Chroma(
    embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001"),
    persist_directory='_Vectors/chroma_db',
    collection_name='ipl_players'
)

def add_documents(docs):
    # add documents
    vector_store.add_documents(docs)
    print("Documents added successfully")

def delete_document(ids="09a39dc6-3ba6-4ea7-927e-fdda591da5e4"):
    # delete document
    vector_store.delete(ids=ids)
    print("Document deleted successfully")

def view_documents():
    # view documents
    return vector_store.get(include=['embeddings','documents', 'metadatas'])

def search_documents():
    # search documents
    return vector_store.similarity_search(
        query='Who among these are a bowler?',
        k=2
    )

def metadata_filtering(query= "", team= "Chennai Super Kings"):
    # meta-data filtering
    return vector_store.similarity_search_with_score(
        query=query,
        filter={"team": team}
    )

def update_documents(document_id="09a39dc6-3ba6-4ea7-927e-fdda591da5e4"):
    # update documents
    updated_doc1 = Document(
        page_content="Virat Kohli, the former captain of Royal Challengers Bangalore (RCB), is renowned for his aggressive leadership and consistent batting performances. He holds the record for the most runs in IPL history, including multiple centuries in a single season. Despite RCB not winning an IPL title under his captaincy, Kohli's passion and fitness set a benchmark for the league. His ability to chase targets and anchor innings has made him one of the most dependable players in T20 cricket.",
        metadata={"team": "Royal Challengers Bangalore"}
    )
    vector_store.update_document(document_id=document_id, document=updated_doc1)
    print("Document updated successfully")

if __name__ == "__main__":
    while 1:
        option = input("""1) Add documents
2) View documents
3) Search documents
4) Meta-data filtering
5) Update documents
6) Delete document
7) Exit\n\n
        Enter option: """)

        if option == "1":
            add_documents(docs)
        elif option == "2":
            data = view_documents()
            print("length of data:", len(data.get("documents")))
            print(data)
        elif option == "3":
            for e in search_documents():
                print(e)
        elif option == "4":
            for e in metadata_filtering(query="", team="Chennai Super Kings"):
                print(e)
        elif option == "5":
            update_documents(document_id="5c582778-2652-4cdb-b090-9c5989e605c5")
        elif option == "6":
            delete_document(ids="5c582778-2652-4cdb-b090-9c5989e605c5")
        elif option == "7":
            break
        