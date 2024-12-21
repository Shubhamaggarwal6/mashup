import os
from youtubesearchpython import VideosSearch
import yt_dlp

def clear_downloads_folder(folder='downloads'):
    """Remove all files from the downloads folder."""
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"Cleared the '{folder}' folder.")
def download_audio(keyword, max_videos=4):
    # Create a folder to store downloads if it doesn't exist
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    else:
        clear_downloads_folder(folder='downloads')


    # Search for videos on YouTube with the given keyword
    videos_search = VideosSearch(keyword, limit=max_videos)
    videos_result = videos_search.result()

    # Check if videos are found
    if not videos_result['result']:
        print(f"No videos found for keyword: {keyword}")
        return

    # Process each video found
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


# if __name__ == "__main__":
keyword = input("Enter the keyword for YouTube video search: ")
download_audio(keyword)
