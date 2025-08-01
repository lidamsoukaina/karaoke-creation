#!/bin/bash

#############################################################################
echo "[STEP 1] Audio Acquisition..." 
# check if the virtual environment exists
if [ ! -d "envs/get-audio-venv" ]; then
    echo "Creating virtual environment..."
    python -m venv envs/get-audio-venv 
    source envs/get-audio-venv/bin/activate
    pip install -r requirements/get_audio_requirements.txt 
else
    source envs/get-audio-venv/bin/activate
    echo "Virtual environment already exists."
fi

# Example: python get_audio.py https://youtu.be/u2ah9tWTkmk\?si\=Un2ZfOzGD9FC4fyF wav outputs/ordinary-audio
read -p "Enter YouTube URL: " url
read -p "Enter output path (default: outputs/downloaded-audio): " output_dir
python get_audio.py "${url:-https://youtu.be/u2ah9tWTkmk\?si\=Un2ZfOzGD9FC4fyF}" wav "${output_dir:-outputs/downloaded-audio}"
output_audio_file="${output_dir:-outputs/downloaded-audio}.wav"
echo "---> ✅ Audio Acquisition completed. Output file: $output_audio_file"
deactivate

#############################################################################
echo "[STEP2] Vocals and Instruments Separation..." 
# check if the virtual environment exists
if [ ! -d "envs/separate-venv" ]; then
    echo "Creating virtual environment..."
    python -m venv envs/separate-venv
    source envs/separate-venv/bin/activate
    pip install -r requirements/separate_vocals_and_instruments_requirements.txt
else
    source envs/separate-venv/bin/activate
    echo "Virtual environment already exists and activated."
fi
output_audio_dir=$(dirname "$output_audio_file")
python separate_vocals_and_instruments.py "$output_audio_file" "${output_audio_dir}"
echo "---> ✅ Vocals and Instruments Separation completed. Output files are in: ${output_dir:-outputs/downloaded-audio}"
deactivate

#############################################################################
echo "[STEP3] Transcribing Audio..."
# check if the virtual environment exists
if [ ! -d "envs/transcribe-venv" ]; then
    echo "Creating virtual environment..."
    python -m venv envs/transcribe-venv
    source envs/transcribe-venv/bin/activate
else
    source envs/transcribe-venv/bin/activate
    echo "Virtual environment already exists and activated."
fi
# check that that the vocals file exists
vocals_file="${output_dir:-outputs/downloaded-audio}/vocals.wav"
if [ ! -f "$vocals_file" ]; then
    echo "Vocals file not found: $vocals_file"
    exit 1
fi
#  uvx whisperx --model medium --device cpu outputs/ordinary-audio/vocals.wav --compute_type float32
uvx whisperx --model medium --device cpu "$vocals_file" --compute_type float32 --output_dir "${output_audio_dir:-outputs}/transcriptions" --output_format json
deactivate
echo "---> ✅ Transcription completed. Output file: ${output_audio_dir:-outputs/downloaded-audio}/transcriptions/vocals.json"

#############################################################################
echo "[STEP4] Generating Karaoke Video..."
echo "[STEP4.1] Generating Ass File..."
python get_ass.py  "$output_audio_dir/transcriptions/vocals.json" "$output_audio_dir/transcriptions/subtitles.ass"
echo "---> ✅ Generating ass file completed. subtitles available at ${output_audio_dir}/transcriptions/subtitles.ass"
echo "[STEP4.2] Creating background Video..."
DURATION=$(ffprobe -i $output_audio_file -show_entries format=duration -v quiet -of csv="p=0")
ffmpeg -f lavfi -i color=c=black:s=1280x720:d=$DURATION -i "${output_dir:-outputs/downloaded-audio}/accompaniment.wav" -c:v libx264 -c:a aac -shortest "${output_dir:-outputs/downloaded-audio}/black_video_with_accompaniment.mp4"
echo "---> ✅ Generating background video completed. Video available at ${output_dir:-outputs/downloaded-audio}/black_video_with_accompaniment.mp4"

echo "[STEP4.3] Merging ass and background video..."
ffmpeg -y -i "${output_dir:-outputs/downloaded-audio}/black_video_with_accompaniment.mp4" -vf "ass=$output_audio_dir/transcriptions/subtitles.ass" -c:a copy "final_karaoke_video.mp4"
echo "---> ✅ Generating karaoke video completed. Video available at final_karaoke_video.mp4"

#TODO: add this for black video: ffmpeg -i black_video.mp4 -i outputs/ordinary-audio/accompaniment.wav -c:v copy -c:a aac -shortest black_video_with_accompaniment.mp4 
# echo "Audio duration: $DURATION seconds"

# echo "Black video with accompaniment created: $output_dir/black_video_with_accompaniment.mp4"

echo "finished"