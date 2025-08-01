from spleeter.separator import Separator
import os


def separate_vocals_instruments(audio_file, output_dir):
    # check if the output directory exists, if not create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # check if the audio file exists
    if not os.path.isfile(audio_file):
        raise FileNotFoundError(f"The audio file {audio_file} does not exist.")

    # Load Spleeter model
    print("Loading Spleeter model...")
    separator = Separator("spleeter:2stems")

    # Separate vocals and instruments
    print("Separating audio with Spleeter...")
    separator.separate_to_file(audio_file, output_dir)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print(
            "Usage: python separate_vocals_and_instruments.py <audio_file> <output_dir>"
        )
        sys.exit(1)

    audio_file = sys.argv[1]
    output_dir = sys.argv[2]

    separate_vocals_instruments(audio_file, output_dir)
