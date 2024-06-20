from pytube import YouTube
import youtube_dl
import ssl

def download_video(url):
    ssl._create_default_https_context = ssl._create_unverified_context
    yt = YouTube(url)
    video = yt.streams.first()
    video.download('media')

    # ydl_opts = {}
    # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #     ydl.download([url])

download_video('https://www.youtube.com/watch?v=WQpnRmZRHFE')