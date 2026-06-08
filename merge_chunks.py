import os
import json
import math

jsons = os.listdir('jsons')
n = 5
for json_file in jsons:
    with open(os.path.join('jsons', json_file), 'r') as f:
        content = json.load(f)
        total_chunks = len(content["chunks"])
        chunks_group = math.ceil(total_chunks / n)
        print(f"{total_chunks} chunks in {json_file}, grouped into {chunks_group} groups")
        newchunks = []
        for i in range(chunks_group):
            start = i*n
            end = min((i+1)*n, total_chunks)
            chunk_group = content["chunks"][start:end]
            newchunks.append({
                "number" : i,
                "title": chunk_group[0]["title"],
                "start": chunk_group[0]["start"],
                "end": chunk_group[-1]["end"],
                "text": " ".join([chunk["text"] for chunk in chunk_group])
            })
            os.makedirs('merged_jsons', exist_ok=True)
            with open(os.path.join('merged_jsons', json_file), 'w') as f:
                json.dump({
                    "chunks": newchunks,
                    "text": content["text"]
                }, f, indent=4)