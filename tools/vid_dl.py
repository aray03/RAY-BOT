from __future__ import annotations
from langchain_core.tools import tool
from config import VID_DOWNLOAD_PATH
import yt_dlp

"""
Downloads a video or audio from a given URL using yt-dlp.
This tool is designed to handle various video and audio formats, providing a simple interface for downloading content.


"""


@tool
def download_video(video_url: str, audio_only: bool = False) -> str:
    """Downloads a video or audio from a given URL using yt-dlp.

    Args:
        video_url: The URL of the video or audio to download.
        audio_only: If True, downloads only the audio. Defaults to False.

        Returns:
            The path to the downloaded file.
    """

    ydl_opts = {
        "format": "bestaudio/best" if audio_only else "bestvideo+best",
        "outtmpl": f"{VID_DOWNLOAD_PATH}/%(title)s.%(ext)s",
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        value = ydl.download([video_url])

    return value
