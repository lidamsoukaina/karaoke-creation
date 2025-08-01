import whisperx
import torch
from typing import List, Dict

def transcribe_with_whisperx(
    audio_path: str,
    model_size: str = "medium",
    return_segments: bool = False,
    save_to_json: str = None
) -> List[Dict]:
    """
    Transcribe audio and return word-level timestamped transcript using WhisperX.

    Args:
        audio_path (str): Path to audio file (e.g., .wav or .mp3)
        model_size (str): Whisper model size ("tiny", "base", "small", "medium", "large")
        return_segments (bool): Whether to return segment-level output in addition to words
        save_to_json (str): Optional path to save word segments to a JSON file

    Returns:
        List[Dict]: A list of word segments with 'word', 'start', 'end', 'score'
    """

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[INFO] Using device: {device}")

    # Load Whisper model
    model = whisperx.load_model(model_size, device)

    print("[INFO] Transcribing audio...")
    result = model.transcribe(audio_path)

    # Load alignment model
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)

    # Align to word level
    aligned_result = whisperx.align(result["segments"], model_a, metadata, audio_path, device)

    word_segments = aligned_result["word_segments"]

    if save_to_json:
        import json
        with open(save_to_json, "w", encoding="utf-8") as f:
            json.dump(word_segments, f, indent=2, ensure_ascii=False)
        print(f"[INFO] Word-level transcript saved to {save_to_json}")

    if return_segments:
        return word_segments, result["segments"]

    return word_segments

if __name__ == "__main__":
    words = transcribe_with_whisperx("outputs/downloaded-audio/vocals.wav", save_to_json="outputs/lyrics.json")
    for word in words[:10]:
        print(word)