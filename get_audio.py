import os
import sys
import yt_dlp as youtube_dl
import tempfile
import logging


def download_audio(youtube_url, output_format="wav", output_path=None):
    """
    Downloads audio from a YouTube video and saves it in the specified format.

    :param youtube_url: str, URL of the YouTube video
    :param output_format: str, format to save the audio file (default is 'wav')
    :param output_path: str, path where to save the audio file (optional)
    :return: str, path to the saved audio file
    """
    if output_format not in ["wav", "mp3"]:
        raise ValueError("Unsupported output format. Use 'wav' or 'mp3'.")

    if output_path:
        if os.path.isdir(output_path):
            outtmpl = os.path.join(output_path, "%(title)s.%(ext)s")
        else:
            outtmpl = output_path
    else:
        outtmpl = os.path.join(tempfile.gettempdir(), "%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": output_format,
                "preferredquality": "192",
            }
        ],
        "outtmpl": outtmpl,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        filename = ydl.prepare_filename(info)

    if output_path and not os.path.isdir(output_path):
        base_path = os.path.splitext(output_path)[0]
        return f"{base_path}.{output_format}"
    else:
        return filename.replace(".webm", f".{output_format}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_audio.py <youtube_url> [output_format] [output_path]")
        print("  youtube_url: URL of the YouTube video")
        print("  output_format: 'wav' or 'mp3' (default: 'wav')")
        print("  output_path: Path where to save the audio file (optional)")
        print("               Can be a directory or a specific file path")
        sys.exit(1)

    youtube_url = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else "wav"
    output_path = sys.argv[3] if len(sys.argv) > 3 else None

    try:
        audio_file = download_audio(youtube_url, output_format, output_path)
        print(f"Audio downloaded and saved as: {audio_file}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)
