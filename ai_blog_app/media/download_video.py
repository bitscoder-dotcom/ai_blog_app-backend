from pytube import YouTube
import ssl
from moviepy.editor import AudioFileClip
import os

# def download_video(url):
#     ssl._create_default_https_context = ssl._create_unverified_context
#     yt = YouTube(url)
#     video = yt.streams.first()
#     video.download('media')

# download_video('https://www.youtube.com/watch?v=WQpnRmZRHFE')

def download_audio(link):
    print("Starting the download process...")
    ssl._create_default_https_context = ssl._create_unverified_context
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    print("Video fetched successfully...")
    out_file = video.download(output_path='media')
    print(f"Audio downloaded and saved as {out_file}...")
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    
    # Convert the audio file to mp3
    print("Converting the audio to mp3...")
    audio = AudioFileClip(out_file)
    audio.write_audiofile(new_file)
    print(f"Audio converted and saved as {new_file}...")
    
    # Remove the original audio file
    print("Removing the original audio file...")
    os.remove(out_file)
    print("Original audio file removed...")
    
    print("Download process completed successfully!")
    return new_file

# download_audio('https://www.youtube.com/watch?v=WQpnRmZRHFE')

def find_large_files(directory, size_limit_mb):
    # Convert size limit from MB to bytes
    size_limit = size_limit_mb * 1024 * 1024

    # Initialize a list to store the paths of the files that exceed the size limit
    large_files = []

    # Walk through the directory
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            # Get the path of the file
            file_path = os.path.join(foldername, filename)
            # Get the size of the file
            file_size = os.path.getsize(file_path)
            # If the file size exceeds the size limit, add it to the list
            if file_size > size_limit:
                large_files.append(file_path)

    # Return the paths of the large files
    return large_files

# Example usage:
large_files = find_large_files(".", 20)
for file_path in large_files:
    print(f"The file {file_path} is larger than 20 MB.")

find_large_files('AI_BLOG_APP', 20)