import os
from pydub import AudioSegment

def convert_mp3_to_wav(input_file, output_file):
    try:
        # Check if the MP3 file exists
        if not os.path.exists(input_file):
            print(f"Error: The file '{input_file}' was not found.")
            return False

        # Load the MP3 audio file
        mp3_audio = AudioSegment.from_file(input_file, format="mp3")

        # Export the audio to WAV format
        mp3_audio.export(output_file, format="wav")
        print(f"Conversion successful: '{output_file}' created.")
        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def split_audio(input_file, output_directory, chunk_length_ms=2 * 60 * 1000):
    try:
        # Check if the WAV file exists
        if not os.path.exists(input_file):
            print(f"Error: The file '{input_file}' was not found.")
            return

        # Load the WAV file
        audio = AudioSegment.from_file(input_file, format="wav")

        # Create output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)

        # Split audio into chunks and save each one
        for i, start in enumerate(range(0, len(audio), chunk_length_ms), start=1):
            chunk = audio[start:start + chunk_length_ms]
            output_path = os.path.join(output_directory, f"{i}_audio_file.wav")
            chunk.export(output_path, format="wav")
            print(f"Saved: {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")