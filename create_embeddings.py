#ollama msut be installed
#ollama pull bge-m3 must be run to pull the model
import requests
import os
import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def create_embeddings(text_list):
    response = requests.post("http://localhost:11434/api/embed", json={
        "model": "bge-m3",
        "input": text_list
    })
    embeddings = response.json()["embeddings"]
    return embeddings


jsons = os.listdir("jsons")
my_dict = []
if not os.path.exists("json_embeddings"):
    os.makedirs("json_embeddings")
    
    
    for json_file in jsons:
        with open(os.path.join("jsons", json_file), "r") as f:
            content = json.load(f)
        text_list = [c["text"] for c in content["chunks"]] 
        embeddings = create_embeddings(text_list)

        for i,chunk in enumerate(content["chunks"]):
            chunk['embedding'] = embeddings[i]
            my_dict.append(chunk)

        with open(os.path.join("json_embeddings", json_file), "w") as f:
            json.dump(content, f)

    df = pd.DataFrame.from_records(my_dict)
    print(df)

else:
    print("Embeddings already created. Loading from json_embeddings folder.")
    jsons = os.listdir("json_embeddings")
    for json_file in jsons:
        with open(os.path.join("json_embeddings", json_file), "r") as f:
            content = json.load(f)
        for chunk in content["chunks"]:
            my_dict.append(chunk)

    df = pd.DataFrame.from_records(my_dict)
    print(df)

incoming_query = input("Ask a Question: ")
question_embedding = create_embeddings([incoming_query])

similarities = cosine_similarity(
    np.vstack(df["embedding"].values),
    np.array(question_embedding)
).flatten()
top_results = 5
result_indx = similarities.argsort()[-top_results:][::-1]

new_df = df.loc[result_indx]