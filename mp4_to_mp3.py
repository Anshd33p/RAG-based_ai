import os
import subprocess

files= os.listdir('videos')

def convert_video_interval_to_audio(input_path, output_path, start_time, duration):
    subprocess.run([
        "ffmpeg",
        "-ss", str(start_time),
        "-i", input_path,
        "-t", str(duration),
        "-vn",
        output_path,
    ])

for file in files:
    file_name = file.split('.')[0]
    subprocess.run(["ffmpeg", "-i", f"videos/{file}", f"audios/{file_name}.mp3"])
    # convert_video_interval_to_audio(
    #     f"videos/{file}",
    #     f"audios/{file_name}.mp3",
    #     start_time="00:01:00",
    #     duration="00:00:30",
    # )
    print(f"Processed {file}")