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

def inference(prompt):
    r = requests.post("http://localhost:11434/api/generate", json={
        # "model": "deepseek-r1",
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    })
    
    return r.json()["response"]

df = joblib.load('embeddings.joblib')
incoming_query = input("Ask a Question: ")
question_embedding = create_embedding([incoming_query])[0]
similarities = cosine_similarity(np.vstack(df['embedding']), [question_embedding]).flatten()

top_results = 10
result_indx = similarities.argsort()[-top_results:][::-1]

new_df = df.loc[result_indx]
prompt = f'''Here are video subtitle chunks containing video title, video number, start time in seconds, end time in seconds, the text at that time:

{new_df[["title", "number", "start", "end", "text"]].to_json(orient="records")}
---------------------------------
"{incoming_query}"
User asked this question related to the video chunks, you have to answer in a human way (by analyzing all chunks(like where it is mostly mentioned))and tell which video might contain the needed information (don't mention chunk number) by giving the title(you can see that many chunks have same title which means they are part of same video) and the timestamp(may merge with other and convert to minutes). (this output will be directly shared to the user so don't say any words describing the data(like chunks or anything) just mention the title timestamp and the reasoning)
'''
response = inference(prompt)
print(response)