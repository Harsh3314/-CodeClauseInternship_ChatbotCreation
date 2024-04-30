import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import random
import spacy
from nltk.metrics import jaccard_distance

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

nlp = spacy.load("en_core_web_md")

training_data = [
    {"patterns": ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"],
     "responses": ["Hello!", "Hi there!", "Hey!", "Good morning!", "Good afternoon!", "Good evening!"]},
    
    {"patterns": ["what's your name?", "who are you?", "tell me about yourself"],
     "responses": ["I'm a chatbot.", "You can call me Chatbot.", "I'm here to assist you with any questions."]},
    
    {"patterns": ["bye", "goodbye", "see you later", "see you soon", "take care"],
     "responses": ["Goodbye!", "See you later!", "Take care!"]},
    
    {"patterns": ["what can you do?", "what are your capabilities?", "what do you do?", "how can you help me?"],
     "responses": ["I can answer questions, provide information, and engage in conversation."]},
    
    {"patterns": ["thank you", "thanks", "appreciate it"],
     "responses": ["You're welcome!", "No problem!", "My pleasure!"]},
]

def preprocess(text):
    tokens = word_tokenize(text.lower())  
    tokens = [word for word in tokens if word.isalnum()]  
    tokens = [word for word in tokens if word not in stopwords.words('english')]  
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]  
    return tokens

def train_chatbot(training_data):
    train_data_spacy = []
    for entry in training_data:
        for pattern in entry['patterns']:
            tokens = preprocess(pattern)
            train_data_spacy.append((pattern, {'response': entry['responses'][0]}))
    return train_data_spacy

train_data_spacy = train_chatbot(training_data)

for text, annotations in train_data_spacy:
    for ent in annotations.get('entities', []):
        ner.add_label(ent[2])

while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        break  
    user_tokens = set(preprocess(user_input))  
    matched_response = None
    max_similarity = 0
    for pattern, response in train_data_spacy:
        pattern_tokens = set(preprocess(pattern))
        if pattern_tokens:  
            similarity = 1 - jaccard_distance(pattern_tokens, user_tokens)
            if similarity > max_similarity:  
                max_similarity = similarity
                matched_response = response['response']
   
    if max_similarity > 0.9:  
        print("Bot:", matched_response)
    else:
        print("Bot: Sorry, I don't understand that.")