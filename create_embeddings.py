#ollama msut be installed
#ollama pull bge-m3 must be run to pull the model
import requests
def create_embeddings(prompt):
    response = requests.post("http://localhost:11434/api/embeddings", json={
        "model": "bge-m3",
        "prompt": prompt
    })
    return response.json()["embedding"]

response = create_embeddings("What is RAG-based AI?")
print(response)