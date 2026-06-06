import json
import os
import whisper
model = whisper.load_model("large-v2")

audios = os.listdir("audios")
for audio in audios:
    result= model.transcribe(audio= f"audios/{audio}",
                             language="hindi",
                             word_timestamps=False)
    
    segments = result["segments"]
    chunks = []
    for segment in segments:
        chunks.append({
            "number": segment["id"],
            "title": audio.split(".")[0],
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"]
        })
        result_metadata = {
            "chunks": chunks,
            "text": result["text"]
        }
    with open(f"jsons/{audio.split('.')[0]}.json", "w") as f:
        json.dump(result_metadata, f)