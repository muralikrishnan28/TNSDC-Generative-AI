from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

#for Chatbot
from django.conf import settings
import os
import json 
import numpy as np
from tensorflow import keras
import pickle
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

@csrf_exempt
def chat(request):
    if request.method == 'GET':
        response = 'Hello! Welcome, How can I assist you today?'
        return render(request, 'chatbot/chatbot.html', {'response': response})
    else:
        inp = request.POST['query']
        print(inp)
        file_path = os.path.join(settings.BASE_DIR, 'utility files', 'dataset.json')
        with open(file_path) as file:
            data = json.load(file)

        # load trained model
        model = keras.models.load_model(os.path.join(settings.BASE_DIR, 'utility files', 'chat_model.h5'))

        # load tokenizer object
        with open(os.path.join(settings.BASE_DIR, 'utility files', 'tokenizer.pickle'), 'rb') as handle:
            tokenizer = pickle.load(handle)
        
        # load label encoder object
        with open(os.path.join(settings.BASE_DIR, 'utility files', 'label_encoder.pickle'), 'rb') as enc:
            lbl_encoder = pickle.load(enc)

        # parameters
        max_len = 200

        preprocessed_input = preprocess_text(inp)
        sequence = tokenizer.texts_to_sequences([preprocessed_input])
        padded_sequence = keras.preprocessing.sequence.pad_sequences(sequence, truncating='post', maxlen=max_len)
        result = model.predict(padded_sequence)
        tag = lbl_encoder.inverse_transform([np.argmax(result)])
        probability = np.max(result)

        for i in data['questions']:
            if (len(i['tags'])>0):
                if i['tags'][0] == tag:
                    response = {'response': i['answer'], 'score': str(probability)}
                    return JsonResponse(response)
                    

def preprocess_text(text):
    # Load stop words
    stop_words = set(stopwords.words('english'))

    # Initialize lemmatizer
    lemmatizer = WordNetLemmatizer()

    # Remove special characters and numbers
    text = re.sub('[^a-zA-Z]', ' ', text)
    
    # Tokenize the text
    words = nltk.word_tokenize(text)
    
    # Lemmatize and remove stop words
    words = [lemmatizer.lemmatize(word.lower()) for word in words if word.lower() not in stop_words]
    
    return ' '.join(words)