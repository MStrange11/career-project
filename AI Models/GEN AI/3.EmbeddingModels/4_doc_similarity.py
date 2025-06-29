from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

embeddings = OpenAIEmbeddings(model="text-embedding-3-large", dimensions=300)

document = [
"Virat Kohli is an Indian cricketer known for his aggressive batting and leadership.",
"MS Dhoni is a former Indian captain famous for his calm demeanor and finishing skills.",
"Sachin Tendulkar, also known as the 'God of Cricket', holds many batting records.",
"Rohit Sharma is known for his elegant batting and record-breaking double centuries.",
"Jasprit Bumrah is an Indian fast bowler known for his unorthodox action and yorkers."
]

query = "tell me about Virat Kohli"

# Example output of similarity_scores: [[0.66305456 0.34860867 0.34340637 0.39610939 0.3951678 ]]
# means query is most similar to the first document with a score of 0.66305456


try:
    document_embeddings = embeddings.embed_documents(document)
    query_embedding = embeddings.embed_query(query)

    similarity_scores = cosine_similarity([query_embedding], document_embeddings)[0]

    index, score = sorted(list(enumerate(similarity_scores)), key=lambda x: x[1], reverse=True)[0:3]

    print(f"Top 3 most similar documents to the query '{query}':")
    for i, (idx, score) in enumerate(zip(index, score)):
        print(f"{i+1}. {document[idx]} (Score: {score:.4f})")
except Exception as e:
    if "429" in str(e):
        res = "Rate limit exceeded. Please try again later. Upgrading your plan."
        print(res)
    else:
        print(f"An error occurred: {str(e)}")