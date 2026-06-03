import joblib
import requests
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def create_embedding(text_list):
    response = requests.post("http://localhost:11434/api/embed", json={
        "model": "bge-m3",
        "input": text_list
    })
    embeddings = response.json()["embeddings"]
    return embeddings

df = joblib.load('embeddings.joblib')
incoming_query = input("Ask a Question: ")
question_embedding = create_embedding([incoming_query])[0]
similarities = cosine_similarity(np.vstack(df['embedding']), [question_embedding]).flatten()

top_results = 5
result_indx = similarities.argsort()[-top_results:][::-1]

new_df = df.loc[result_indx]
print(new_df[["title", "number", "text"]])