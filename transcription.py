import os
import spacy
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import librosa
import numpy as np
from keybert import KeyBERT
import logging
from collections import Counter
import string
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the SpaCy model for Named Entity Recognition (NER)
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    logger.error(f"Error loading SpaCy model: {str(e)}")
    raise Exception("Failed to load SpaCy model. Please ensure it's installed with 'python -m spacy download en_core_web_sm'")

# Load the pre-trained Wav2Vec2 model and processor
try:
    processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")
except Exception as e:
    logger.error(f"Error loading Wav2Vec2 model: {str(e)}")
    raise Exception("Failed to load Wav2Vec2 model")

def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Fix common transcription errors
    text = text.replace(" i ", " I ")
    text = re.sub(r'\bi\b', 'I', text)
    
    # Capitalize first letter of sentences
    text = '. '.join(s.capitalize() for s in text.split('. '))
    
    # Capitalize proper nouns (basic approach)
    proper_nouns = ['arwin', 'ransal']  # Add more as needed
    for noun in proper_nouns:
        text = text.replace(noun.lower(), noun.capitalize())
    
    return text

def extract_frequent_words(text, top_n=5):
    # Convert to lowercase and remove punctuation
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Split into words
    words = text.split()
    
    # Remove common stop words and short words
    stop_words = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", 
                     "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 
                     'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 
                     'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 
                     'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 
                     'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 
                     'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 
                     'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 
                     'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 
                     'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 
                     'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 
                     'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
                     'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will',
                     'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're',
                     've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn',
                     "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",
                     'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan',
                     "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won',
                     "won't", 'wouldn', "wouldn't", 'going', 'talk', 'day'])
    
    words = [word for word in words if word not in stop_words and len(word) > 3]
    
    # Count word frequencies
    word_freq = Counter(words)
    
    # Get the top N most frequent words
    return [word for word, freq in word_freq.most_common(top_n)]

def transcribe_audio_file(audio_path):
    try:
        logger.info(f"Processing audio file: {audio_path}")
        
        # Verify file exists
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
        # Load and process the audio
        audio, sr = librosa.load(audio_path, sr=16000)
        logger.info("Audio file loaded successfully")
        
        # Ensure audio data is valid
        if len(audio) == 0:
            raise ValueError("Audio file is empty or corrupted")
            
        inputs = processor(audio, sampling_rate=sr, return_tensors="pt", padding=True)
        
        # Perform speech-to-text with Wav2Vec2
        with torch.no_grad():
            logits = model(input_values=inputs.input_values).logits
        
        # Decode the logits to get the transcription text
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.decode(predicted_ids[0])
        logger.info("Transcription completed successfully")

        if not transcription.strip():
            raise ValueError("Transcription is empty")

        # Clean and format the transcription
        transcription = clean_text(transcription)
        logger.info("Transcription cleaned and formatted")

        # Initialize keyword extractors
        kw_model = KeyBERT()

        # 1. Named Entity Recognition using SpaCy
        doc = nlp(transcription)
        named_entities = [(ent.text, ent.label_) for ent in doc.ents]
        logger.info(f"Found {len(named_entities)} named entities")
        
        # 2. Extract keywords using KeyBERT
        keybert_keywords = kw_model.extract_keywords(transcription, 
                                                   keyphrase_ngram_range=(1, 2),
                                                   stop_words='english',
                                                   top_n=5,
                                                   use_maxsum=True,
                                                   diversity=0.7)
        logger.info(f"Extracted {len(keybert_keywords)} key phrases")
        
        # 3. Extract frequent words
        frequent_words = extract_frequent_words(transcription)
        logger.info(f"Extracted {len(frequent_words)} frequent words")
        
        # Combine all keywords
        all_keywords = {
            'named_entities': named_entities,
            'key_phrases': [kw[0] for kw in keybert_keywords],
            'frequent_words': frequent_words
        }
        
        logger.info("Keyword extraction completed successfully")
        logger.info(f"Keywords found: {all_keywords}")
        
        return transcription, all_keywords

    except Exception as e:
        logger.error(f"Error in transcribe_audio_file: {str(e)}")
        raise Exception(f"Failed to process audio file: {str(e)}")