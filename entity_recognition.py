import spacy

# Load SpaCy model for Named Entity Recognition (NER)
try:
    nlp = spacy.load("en_core_web_lg")
    print("SpaCy NER model loaded successfully.")
except Exception as e:
    print(f"Error loading SpaCy model: {e}")

def perform_ner(text):
    """
    Performs Named Entity Recognition on the provided text.
    """
    doc = nlp(text.lower())
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    print("\nEntities:", entities)
    return entities