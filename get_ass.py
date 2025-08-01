import json
from datetime import timedelta

# === CONFIG ===
FONT_NAME = "Amiri"
FONT_SIZE = 48
VIDEO_RES = (1280, 720)


def seconds_to_timestamp(seconds):
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    cs = int((td.total_seconds() - total_seconds) * 100)
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    return f"{h}:{m:02}:{s:02}.{cs:02}"


def generate_ass_header():
    width, height = VIDEO_RES
    return f"""[Script Info]
Title: Arabic Karaoke
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{FONT_NAME},{FONT_SIZE},&H00FFFFFF,&H000000FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,2,1,5,20,20,30,1
Style: Highlight,{FONT_NAME},{FONT_SIZE},&H0000FFFF,&H000000FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,2,1,5,20,20,30,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def format_word_dialogue(start, end, words, highlight_idx):
    # Use ASS karaoke tags for progressive highlighting
    karaoke_parts = []
    for i, word in enumerate(words):
        w = word["word"]
        # Duration in centiseconds for \k tag
        duration_cs = int((word["end"] - word["start"]) * 100)
        karaoke_parts.append(f"{{\\k{duration_cs}}}{w}")
    line = " ".join(karaoke_parts)
    return line


def convert_whisperx_json_to_ass(json_path, ass_output_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    segments = data["segments"]

    header = generate_ass_header()
    dialogue_lines = []

    for seg in segments:
        words = seg["words"]
        if not words:
            continue
        start = seconds_to_timestamp(words[0]["start"])
        end = seconds_to_timestamp(words[-1]["end"])
        line = format_word_dialogue(start, end, words, 0)
        dialogue_lines.append(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{line}")

    with open(ass_output_path, "w", encoding="utf-8") as f:
        f.write(header)
        f.write("\n".join(dialogue_lines))

    print(f"✅ ASS subtitle written to: {ass_output_path}")


# === USAGE ===
# convert_whisperx_json_to_ass("outputs/transcriptions/vocals.json", "outputs/transcriptions/v2-subtitles.ass")
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print(
            "Usage: python json_to_ass.py <json_path> <ass_path>"
        )
        sys.exit(1)

    json_path = sys.argv[1]
    ass_path = sys.argv[2]

    convert_whisperx_json_to_ass(json_path, ass_path)