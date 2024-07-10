# import os

# from gtts import gTTS

# tts = gTTS(text="hello mahendra ,vishal and devendra", lang='en')
# tts.save("pcvoice.mp3")
# # to start the file from python
# os.system("start pcvoice.mp3")

# =========================================================================

# import pyttsx3

# engine = pyttsx3.init()
# volume = engine.getProperty('volume')
# engine.setProperty('volume', 0.9)
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[2].id)
# rate = engine.getProperty('rate')
# engine.setProperty('rate', 100)
# engine.getProperty(voices)
# engine.say("ओर भाई क्या कर रहे हो ओर सुनाओ हैलो hello  ")
# engine.runAndWait()

# ======================================================================

# from os import path

# from pydub import AudioSegment

# # files                                                                         
# src = "temp.mp3"
# dst = "test.wav"

# # convert wav to mp3                                                            
# sound = AudioSegment.from_mp3(src)
# sound.export(dst, format="wav")

# ============================================================

from gtts.lang import tts_langs

supported_languages = tts_langs()
print(supported_languages,'/n')
