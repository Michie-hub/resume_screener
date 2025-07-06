import spacy
import re

nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text) #removes extra whitespace
    text = re.sub(r'[^\w\s]', '', text) #removes non-ASCII if needed
    if len(text.strip()) == 0:
        print("❌ Warning: Resume text is empty after cleaning!")
    return text