import speech_recognition as spr
from translate import *
from gtts import gTTS
import pyttsx3
import os
from google_speech import *
# def say(text):
#     os.system(f"say {text}")

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
# Creating a recognizer object.
recog = spr.Recognizer()


# Using the mic object created as a source to capture audio
with spr.Microphone() as source:
    speak("Say Hello to initiate the conversation !!")
    print("Say Hello to initiate the conversation !!")
    print("Listening...")    
    
    recog.pause_threshold = 1
    audio = recog.listen(source)
    Text = recog.recognize_google(audio)
    print(Text)
    
    
    # Looking for prompt
    if 'hello' in Text.lower():
        print("\nGot you!!!\n")

        speak("Kindly Choose a Language from below")
        print("Hindi \nFrench \nPunjabi \nJapanese")
        recog.pause_threshold = 1
        audio = recog.listen(source)
        Lang = recog.recognize_google(audio)
        print("\n\n", Lang)
        # Language code to be translated to - can be changed to translate to different languages

        if 'hindi' in Lang.lower():
            to_lang = 'hi'
        elif 'french' in Lang.lower():
            to_lang = 'fr'
        elif 'punjabi' in Lang.lower():
            to_lang = 'pa'
        elif 'japanese' in Lang.lower():
            to_lang = 'ja'
        
        
        # Creating a translator instance
        translator = Translator(to_lang)


        speak("Start speaking, we are translating as you speak !!")
        print("Start speaking, we are translating as you speak !!")
        while True:
            audio = recog.listen(source)
            lines = recog.recognize_google(audio)
            
            print("Here's what we heard :", lines)
            
            # Translating input to selected output language
            translated_lines = translator.translate(lines)
            text = translated_lines
            print("\nThe translated audio should be playing in a few seconds !!")
            print(text)
            
            # Creating a text-to-speech instance
            speak = gTTS(text = text, lang = to_lang, slow = False)
            
            # Saving the output file onto the local computer
            speak.save("output_voice.mp3")
            
            # Playing the saved output (translated) audio file
            os.system("start output_voice.mp3 tempo")