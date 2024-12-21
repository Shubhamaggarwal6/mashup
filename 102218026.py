import sys
import os
from youtubesearchpython import VideosSearch
import yt_dlp
from moviepy.editor import AudioFileClip
import wave
import requests


def clear_downloads_folder(folder='downloads'):
    """Remove all files from the downloads folder."""
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"Cleared the '{folder}' folder.")


def download_audio(keyword, max_videos=4):
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    else:
        clear_downloads_folder(folder='downloads')

    videos_search = VideosSearch(keyword, limit=max_videos)
    videos_result = videos_search.result()

    if not videos_result['result']:
        print(f"No videos found for keyword: {keyword}")
        return

    for i, video in enumerate(videos_result['result']):
        video_url = video['link']
        print(f"Processing video {i + 1}: {video['title']}")

        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'noplaylist': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

            print(f"Processed and added: {video['title']}")

        except Exception as e:
            print(f"Failed to process {video['title']}. Error: {str(e)}")

    downloads_folder = os.path.expanduser("downloads")

    for filename in os.listdir(downloads_folder):
        if filename.endswith(".webm"):
            webm_path = os.path.join(downloads_folder, filename)
            wav_path = os.path.join(downloads_folder, filename.replace(".webm", ".wav"))

            # Convert the file
            audio_clip = AudioFileClip(webm_path)
            audio_clip.write_audiofile(wav_path)

            print(f"Converted {filename} to {wav_path}")


def trim_and_merge_wav_files(input_folder='downloads', output_file='merged_audio.wav', duration=30):
    if os.path.exists(output_file):
        os.remove(output_file)

    output_wave = None

    try:
        for filename in os.listdir(input_folder):
            if filename.endswith('.wav'):
                file_path = os.path.join(input_folder, filename)

                with wave.open(file_path, 'rb') as wav_file:
                    print(f"Processing {file_path}")

                    params = wav_file.getparams()
                    n_channels, sampwidth, framerate, n_frames = params[:4]

                    frames_to_copy = int(framerate * duration)

                    frames = wav_file.readframes(frames_to_copy)

                    if output_wave is None:
                        output_wave = wave.open(output_file, 'wb')
                        output_wave.setparams((n_channels, sampwidth, framerate, 0, 'NONE', 'not compressed'))

                    output_wave.writeframes(frames)

                    print(f"Added {filename} to the merged file.")

        print(f"Combined audio saved as {output_file}.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if output_wave is not None:
            output_wave.close()


def wavtomp3(resultFileName):
    headers = {
        # requests won't add a boundary if this header is set when you pass files=
        # 'Content-Type': 'multipart/form-data',
        'apy-token': 'APY0iQUQRbDAgOFF30V6ETzO0tHnaKh05DjGN5Ii8URG4Rya6O4eFPrR6QYl068MMFy',
    }

    params = {
        'output': 'output.mp3',
    }

    files = {
        'file': open('merged_audio.wav', 'rb'),
    }

    response = requests.post('https://api.apyhub.com/convert/audio/wav-file/mp3-file', params=params, headers=headers,
                             files=files)

    if response.status_code == 200:
        with open(resultFileName, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Error: {response.status_code} - {response.text}")

    files['file'].close()


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Error: Incorrect number of parameters.")
        print("Usage: python 102218041.py <SingerName> <NumberOfVideos> <AudioDuration> <resultFileName>")
    else:
        singer = sys.argv[1]
        n = int(sys.argv[2])
        duration = int(sys.argv[3])
        resultFileName = sys.argv[4]
        download_audio(singer, max_videos=n)
        trim_and_merge_wav_files(duration=duration)
        wavtomp3(str(resultFileName))
