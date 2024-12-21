from moviepy.editor import AudioFileClip
import os

# Path to the Downloads folder
downloads_folder = os.path.expanduser("downloads")

# List all .webm files in the Downloads folder
for filename in os.listdir(downloads_folder):
    if filename.endswith(".webm"):
        webm_path = os.path.join(downloads_folder, filename)
        wav_path = os.path.join(downloads_folder, filename.replace(".webm", ".wav"))

        # Convert the file
        audio_clip = AudioFileClip(webm_path)
        audio_clip.write_audiofile(wav_path)

        print(f"Converted {filename} to {wav_path}")
