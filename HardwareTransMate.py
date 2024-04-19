import speech_recognition as spr
from translate import Translator
import pyttsx3
from gtts import gTTS
import os
import playsound

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)

def say(audio):
    engine.say(audio)
    engine.runAndWait()

def speak(text, lang='en'):
    tts = gTTS(text= text, lang= lang, slow=False)
    tts.save("output.mp3")
    playsound.playsound("output.mp3", True)
    os.remove("output.mp3")

# Creating a recognizer object.
recog = spr.Recognizer()

# Using the mic object created as a source to capture audio
with spr.Microphone() as source:
    say("Say Hello to initiate the conversation !!")
    print("Say Hello to initiate the conversation !!")
    print("Listening...")

    recog.pause_threshold = 0.7
    audio = recog.listen(source)
    text = recog.recognize_google(audio)
    print(text)

    # Looking for prompt
    if 'hello' in text.lower():
        print("\nGot you!!!\n")

        say("Kindly Choose a Language from below")
        print("Hindi \nFrench \nGujarati \nJapanese")
        recog.pause_threshold = 1
        audio = recog.listen(source)
        lang = recog.recognize_google(audio)
        print("\n\n", lang)
        # Language code to be translated to - can be changed to translate to different languages

        if 'hindi' in lang.lower():
            to_lang = 'hi'
        elif 'french' in lang.lower():
            to_lang = 'fr'
        elif 'gujrati' or 'gujarati' in lang.lower():
            to_lang = 'gu'
        elif 'japanese' in lang.lower():
            to_lang = 'ja'

        # Creating a translator instance
        translator = Translator(to_lang)

        say("Start speaking, we are translating as you speak !!")
        print("Start speaking, we are translating as you speak !!")
        
        while True:
            audio = recog.listen(source)
            try:
                lines = recog.recognize_google(audio)
                print("Here's what I heard :", lines)

                # Check if user wants to stop
                if 'stop' in lines.lower():
                    say("Goodbye!")
                    break

                # Translating input to selected output language
                translated_lines = translator.translate(lines)
                speak(translated_lines)
                print("Translated speech:",translated_lines,"\nSpeak Next")
            except spr.UnknownValueError:
                say("TransMate could not understand your voice. Kindly Speak again")
                print("TransMate could not understand your voice. Kindly Speak again")
            except spr.RequestError as e:
                # print("Could not request results from Google Speech Recognition service; {0}".format(e))
                print("Kindly relaunch TransMate!; {0}".format(e))

