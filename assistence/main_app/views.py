import json
import logging
import os

import nltk
import speech_recognition as sr
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from gtts import gTTS
from gtts.lang import tts_langs
from nltk.tokenize import word_tokenize

# Set up logging
logger = logging.getLogger(__name__)

# Ensure NLTK data files are downloaded
nltk.download('punkt')

# Define the supported languages
SUPPORTED_LANGUAGES = list(tts_langs().keys())

# Define commands and responses
COMMANDS_RESPONSES = {
    "hello": "Hi there! How can I assist you today?",
    "what is your name": "I am your Speech Assistant.",
    "how are you": "I am just a program, but I'm here to help you!",
    "tell me a joke": "Why don't scientists trust atoms? Because they make up everything!",
    "हैलो" : "Hi there! How can I assist you today?",
    "तुम्हारा नाम क्या है" : "I am your Speech Assistant."    
    # Add more commands and responses as needed
}

# To store the current language selected by the user
current_language = 'en-IN'  # Default to Indian English

@csrf_exempt
def set_language(request):
    if request.method == 'POST':
        global current_language
        data = json.loads(request.body.decode("utf-8"))
        lang = data.get('language')
        if lang in SUPPORTED_LANGUAGES:
            current_language = lang
            logger.info(f"Language set to: {current_language}")
            return JsonResponse({'status': 'Language set successfully'})
        else:
            return JsonResponse({'error': f'Language not supported: {lang}'})
    return JsonResponse({'error': 'Invalid request'})

@csrf_exempt
def text_to_speech(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        text = data.get('text', '')
        try:
            tts = gTTS(text, lang=current_language)
            audio_path = os.path.join(settings.BASE_DIR, 'static/speech', 'temp.mp3')
            tts.save(audio_path)
            audio_url = settings.STATIC_URL + 'speech/temp.mp3'
            
            return JsonResponse({'status': 'Text-to-speech conversion successful','audio_url': audio_url})
        except Exception as e:
            logger.error(f"Error in text-to-speech conversion: {e}")
            return JsonResponse({'error': 'Text-to-speech conversion failed'})
    return JsonResponse({'error': 'Invalid request'})

@csrf_exempt
def speech_to_text(request):
    if request.method == 'POST':
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            logger.info("Listening for speech...")
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language=current_language)
            tokens = word_tokenize(text)
            save_text_to_file(text)

            # Check if the recognized text matches any commands
            command_response = COMMANDS_RESPONSES.get(text.lower(), "I'm sorry, i can't response this command because this command is not define in my dictionary.")

            # Generate audio response
            tts = gTTS(command_response, lang=current_language, slow=False)
            audio_file_path = os.path.join(settings.BASE_DIR, 'static/speech', 'response.mp3')
            tts.save(audio_file_path)
            audio_url = settings.STATIC_URL + 'speech/response.mp3'

            response_data = {
                'text': text,
                'tokens': tokens,
                'command_response': command_response,
                'audio_url': audio_url
            }
            return JsonResponse(response_data, safe=False)
        except sr.UnknownValueError:
            logger.warning("Could not understand the audio")
            return JsonResponse({'error': 'Could not understand the audio'})
        except sr.RequestError as e:
            logger.error(f"Request Error: {e}")
            return JsonResponse({'error': 'Request error'})
    return JsonResponse({'error': 'Invalid request'})

def save_text_to_file(text):
    output_path = os.path.join(settings.BASE_DIR, 'static/text', 'listion_text.txt')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'a', encoding='utf-8') as file:
        file.write(text + '\n')

def index(request):
    return render(request, 'index.html')
