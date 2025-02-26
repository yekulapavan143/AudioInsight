# 🎙️ AudioInsight

A powerful web application that transforms audio content into actionable insights using advanced speech recognition and natural language processing.

## ✨ Features

- **Audio Transcription**: Convert speech to text with high accuracy
- **Named Entity Recognition**: Automatically identify and classify key entities (people, organizations, locations)
- **Key Phrase Extraction**: Extract the most important phrases and topics
- **Word Frequency Analysis**: Identify the most frequently used words
- **Multiple Audio Format Support**: Handles MP3, WAV, FLAC, and OGG formats
- **User-Friendly Interface**: Clean and intuitive web interface for easy interaction

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Flask web framework
- Required Python packages (install via pip):
  ```bash
  pip install flask
  ```

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yekulapavan143/AudioInsight.git
   cd AudioInsight
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application
   ```bash
   python app.py
   ```

4. Open your web browser and navigate to `http://localhost:5000`

## 🎯 How to Use

1. Access the web interface through your browser
2. Upload your audio file (supported formats: MP3, WAV, FLAC, OGG)
3. Click "Process" to start the analysis
4. View the results:
   - Complete text transcription
   - Named entities found in the audio
   - Key phrases and topics
   - Word frequency analysis

## 🏗️ Project Structure

```
AudioInsight/
├── app.py              # Main Flask application
├── audio_processing.py # Audio processing utilities
├── transcription.py    # Speech-to-text functionality
├── entity_recognition.py # Named entity recognition
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
└── uploads/          # Temporary storage for uploaded files
```

## 🛠️ Technologies Used

- **Flask**: Web framework
- **Python**: Backend processing
- **HTML/CSS/JavaScript**: Frontend interface
- **Natural Language Processing**: For entity recognition and keyword extraction

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/yekulapavan143/AudioInsight/issues).

## 👤 Author

**Yekula Pavan**

* Github: [@yekulapavan143](https://github.com/yekulapavan143)

---
⭐️ Star this project if you find it useful!
