import ollama

embed = ollama.embeddings(
    model="nomic-embed-text",
    prompt="The sky is blue because of Rayleigh scattering"
)

print(embed)