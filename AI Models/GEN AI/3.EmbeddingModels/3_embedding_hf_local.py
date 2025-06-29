from langchain_huggingface import HuggingFaceEmbeddings


emb = HuggingFaceEmbeddings(
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
)

# text = 'Delhi is the capital of India.'

# vector = emb.embed_query(text)
# print(vector, len(vector))


'''
[0.03895361348986626, 0.026190223172307014, -0.040229979902505875, 0.030604945495724678, ...]
total length: 384
'''

documentation = [
    'Delhi is the capital of India.',
    'Paris is the capital of France.',
    'Berlin is the capital of Germany.'
]

vectors = emb.embed_documents(documentation)
print(vectors, len(vectors))
'''
[[0.03895361348986626, 0.026190223172307014, -0.040229979902505875, ...], [0.07395181059837341, 0.016435768455266953, -0.011702912859618664, ...]
, [0.012308408506214619, -0.11706362664699554, 0.06992069631814957, ...]]  # Output: List of vectors for each document in the documentation list

'''