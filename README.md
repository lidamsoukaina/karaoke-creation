## How to Use `run_all.sh`

The `run_all.sh` script automates the process of creating a karaoke video from a YouTube link or local audio file. It handles audio download, vocal/instrument separation, transcription, subtitle generation, and video rendering.

### Prerequisites

- **Python 3.8+** installed on your system.
- **FFmpeg** and **ffprobe** installed and available in your PATH.

### Usage

1. **Make the script executable (if not already):**
   ```sh
   chmod +x run_all.sh
   ```

2. **Run the script:**
   ```sh
   ./run_all.sh
   ```

3. **Follow the prompts:**
   - Enter the YouTube URL when prompted (or press Enter to use the default example).
   - Enter the output directory (or press Enter to use the default: `outputs/downloaded-audio`).

The script will automatically:
  - Set up and activate Python virtual environments for each stage.
  - Download the audio from YouTube.
  - Separate vocals and accompaniment.
  - Transcribe the vocals using WhisperX (ensure `uvx` is installed and available in your environment).
  - Generate subtitles in ASS format.
  - Create a black background video with the accompaniment audio.
  - Overlay the subtitles onto the video to produce the final karaoke video.

### Output Files

- **Audio:** Downloaded and separated audio files in the specified output directory.
- **Transcription:** JSON and ASS subtitle files in `outputs/downloaded-audio/transcriptions/` (or your chosen output directory).
- **Video:**
  - `black_video_with_accompaniment.mp4`: Black background video with accompaniment audio.
  - `final_karaoke_video.mp4`: The final karaoke video with subtitles.

### Example Workflow

```
$ ./run_all.sh
[STEP 1] Audio Acquisition...
Enter YouTube URL: https://youtu.be/your-link
Enter output path (default: outputs/downloaded-audio):
---> ✅ Audio Acquisition completed. Output file: outputs/downloaded-audio.wav
[STEP2] Vocals and Instruments Separation...
---> ✅ Vocals and Instruments Separation completed. Output files are in: outputs/downloaded-audio
[STEP3] Transcribing Audio...
---> ✅ Transcription completed. Output file: outputs/downloaded-audio/transcriptions/vocals.json
[STEP4] Generating Karaoke Video...
---> ✅ Generating ass file completed. subtitles available at outputs/downloaded-audio/transcriptions/subtitles.ass
---> ✅ Generating background video completed. Video available at outputs/downloaded-audio/black_video_with_accompaniment.mp4
---> ✅ Generating karaoke video completed. Video available at final_karaoke_video.mp4
finished
```
