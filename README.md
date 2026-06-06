# RAG-based_ai

This repository contains simple scripts to convert video files to audio, transcribe audio to JSON chunks, create embeddings from those chunks, and run a basic retrieval-augmented generation (RAG) query flow.

## Contents

- `mp4_to_mp3.py` - converts videos in `videos/` to MP3 files in `audios/` using `ffmpeg`.
- `mp3_to_json.py` - transcribes MP3 files in `audios/` to chunked JSON files in `jsons/` using `whisper`.
- `create_embeddings.py` - sends chunk texts to a local embedding API and stores `embeddings.joblib`.
- `process_embeddings.py` - loads `embeddings.joblib`, encodes a user query, finds similar chunks, then queries a local generation API to produce a human-readable answer.
- `embeddings.joblib` - example output produced by `create_embeddings.py`.

Directory structure (important files/folders):

```
audios/       # audio files (mp3)
videos/       # video source files (mp4/...)
jsons/        # transcription outputs from mp3_to_json.py
json_embeddings/ # probably cached or exported json embeddings
embeddings.joblib
*.py          # utility scripts
```

## Prerequisites

- Python 3.8 or newer
- `ffmpeg` installed and available on `PATH` (used by `mp4_to_mp3.py`)
- Internet access for any remote model calls, or a local Ollama server reachable at `http://localhost:11434` running models `llama3.2` and `bge-m3` (the scripts call `/api/embed` and `/api/generate`).

Python packages likely required (install with pip):

```
pandas
numpy
scikit-learn
joblib
requests
whisper   # OpenAI/whisper package or the correct Whisper implementation you're using
# plus any additional packages for audio handling (e.g. pydub) if used locally
```

Note: There is no `requirements.txt` in this repo. You can create one with `pip freeze > requirements.txt` after installing packages, or manually create the file with the list above.

## Setup

1. Clone the repository and change into the project directory.

2. Install needed Python packages:

```bash
pip install pandas numpy scikit-learn joblib requests whisper
```

3. Ensure `ffmpeg` is installed (download from https://ffmpeg.org) and available on `PATH`.

4. If you rely on a local model server for embeddings/generation, ensure it is running and reachable at `http://localhost:11434`. This project expects an Ollama server hosting `llama3.2` (for generation) and `bge-m3` (for embeddings), which are called at `/api/generate` and `/api/embed` respectively.

## Usage

1. Convert videos to audio (MP3):

```powershell
python mp4_to_mp3.py
```

This reads files from `videos/` and writes MP3s to `audios/`.

2. Transcribe audio files to JSON chunks:

```powershell
python mp3_to_json.py
```

This uses the `whisper` model to transcribe each MP3 in `audios/` and writes chunked JSON files to `jsons/`.

3. Create embeddings from the JSON chunk texts:

```powershell
python create_embeddings.py
```

This script sends the chunk text list to `http://localhost:11434/api/embed` (model `bge-m3` by default) and saves a `embeddings.joblib` file.

4. Run a RAG-style query using the precomputed embeddings:

```powershell
python process_embeddings.py
```

Enter your question when prompted. The script computes the query embedding, finds top matching chunks, and posts a combined prompt to `http://localhost:11434/api/generate` (model `llama3.2` by default) to obtain an answer.

## Configuration / Tips

- If you don't have a local embedding/generation server, update the `requests.post` URL calls in `create_embeddings.py` and `process_embeddings.py` to use your hosted model endpoints or API provider.
- Adjust the `model` fields in the scripts to match available models on your server.
- `mp3_to_json.py` currently sets `language="hindi"` for `whisper.transcribe`; change or remove that parameter if you transcribe other languages.

## Troubleshooting

- If `ffmpeg` commands fail, verify `ffmpeg` is installed and accessible from the terminal.
- If `whisper` import fails, ensure you installed the correct Whisper package (the repo expects a `whisper` module).
- If the embedding/generation requests return errors, double-check the server is running at `http://localhost:11434` and the endpoint names and payloads match the server API.

