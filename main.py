from audio_processing import convert_mp3_to_wav, split_audio
from transcription import transcribe_audio_files

# Convert MP3 to WAV
if convert_mp3_to_wav("dnc-2004-speech.mp3", "dnc-2004-speech_converted.wav"):
    # Split the WAV file into chunks
    split_audio("dnc-2004-speech_converted.wav", "audio_chunks")

# Transcribe audio files in the 'audio_chunks' directory
final_transcription, entities = transcribe_audio_files("audio_chunks")

# Print final transcription and entities once
print("\nFinal Transcription:\n",final_transcription)
print("\nEntities:\n",entities)