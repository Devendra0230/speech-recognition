import logging  # for improved error logging
import os  # for creating and saving text files

import nltk
import pyttsx3
import speech_recognition as sr
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from gtts import gTTS
from nltk.tokenize import word_tokenize
from pydub import AudioSegment

from .forms import TextToSpeechForm


#---------------------text to section----------------------
@csrf_exempt
def text_to_speech_view(request):
    if request.method == 'POST':
            text = request.POST.get('gen-speech')
            print(text)
            text = request.body.decode("utf-8")
            print(text)
            
            
            engine = pyttsx3.init()

            female_voice_id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_hiIN_KalpanaM'  # Example ID, replace with your identified female voice ID
            engine.setProperty('voice', female_voice_id)

            engine.setProperty('rate', 150)  
            engine.setProperty('volume', 0.9) 

            # Save the speech to a file
            engine.save_to_file(text, 'static/speech/temp.mp3')
            engine.runAndWait()

            # return render(request, 'index.html', {'audio': 'static/speech/temp.mp3'})
            data = True
            return JsonResponse(data,safe=False)

#---------------speech to text section----------------------

# Download necessary NLTK data files
nltk.download('punkt')

# Define the path for the text file to save recognized text
TEXT_FILE_PATH = os.path.join(os.path.dirname(__file__), 'listion_text.txt')

SUPPORTED_LANGUAGES = ['en-IN']
#     'en-IN','hi-IN', 'te-IN', 'mr-IN', 'ta-IN',
#      'gu-IN', 'pa-IN'
# ]
def setLangueage(lang):
    SUPPORTED_LANGUAGES[0]=lang
    print(SUPPORTED_LANGUAGES)
    return 'done'


@csrf_exempt
def set_language(request):
    lang = request.POST.get('Languages')
    lang = request.body.decode("utf-8")
    setLangueage(lang)
    data = [1]
    return JsonResponse(data,safe=False)    

def index(request):
    return render(request, 'index.html')

def save_text_to_file(text):
    """Append recognized text to a text file with UTF-8 encoding."""
    with open(TEXT_FILE_PATH, 'a', encoding='utf-8') as file:
        file.write(text + '\n')

@csrf_exempt
def speech_to_text(request):
    if request.method == 'POST':
        # Create an instance of Recognizer
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print("Speak Now...")
            audio = r.listen(source)

        try:
                text = r.recognize_google(audio, language=SUPPORTED_LANGUAGES[0])

                # Tokenize the recognized text using NLTK
                tokens = word_tokenize(text)

                # Save the recognized text to a file
                save_text_to_file(text)

                # Return the recognized text and tokens in JSON format
                response_data = {
                    'text': text,
                    'tokens': tokens,
                    'language': SUPPORTED_LANGUAGES  # Include the language in the response
                }
                return JsonResponse(response_data)
        except sr.UnknownValueError:
                logging.warning(f"Could not understand audio for language {SUPPORTED_LANGUAGES}")
        except sr.RequestError as e:
                logging.error(f"Request Error for language {SUPPORTED_LANGUAGES}: {e}")

        return JsonResponse({'text': "Could not understand audio in any supported language"})
    else:
        return JsonResponse({'error': "Invalid request"})

