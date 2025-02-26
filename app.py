from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import subprocess
import tempfile
import shutil
from transcription import transcribe_audio_file

app = Flask(__name__)

# Directory for file uploads
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'wav', 'flac', 'ogg'}  # Add other audio file types if needed

# Check if uploads directory exists, if not create it
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Allowed file extensions for audio files
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('app.html')  # Serve the app.html from the templates folder

@app.route('/process-audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file part'}), 400
    
    file = request.files['audio']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Save the file securely
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the file (transcribe the audio and extract keywords)
        try:
            transcription, keywords = transcribe_audio_file(file_path)

            # Clean up the uploaded file after processing (optional)
            os.remove(file_path)

            # Return the transcription and all extracted keywords
            return jsonify({
                'transcription': transcription,
                'keywords': {
                    'named_entities': [{'text': ent[0], 'type': ent[1]} for ent in keywords['named_entities']],
                    'key_phrases': keywords['key_phrases'],
                    'frequent_words': keywords['frequent_words']
                }
            })

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error details: {error_details}")  # This will show in the Flask console
            return jsonify({'error': f'Error during transcription: {str(e)}\nDetails: {error_details}'}), 500

    else:
        return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)