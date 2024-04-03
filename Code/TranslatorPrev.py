import speech_recognition as spr
from translate import Translator
import pyttsx3

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# Selecting the Hindi voice
for voice in voices:
    if "hindi" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break
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

    recog.pause_threshold = 0.7
    audio = recog.listen(source)
    text = recog.recognize_google(audio)
    print(text)

    # Looking for prompt
    if 'hello' in text.lower():
        print("\nGot you!!!\n")

        speak("Kindly Choose a Language from below")
        print("Hindi \nFrench \nPunjabi \nJapanese")
        recog.pause_threshold = 1
        audio = recog.listen(source)
        lang = recog.recognize_google(audio)
        print("\n\n", lang)
        # Language code to be translated to - can be changed to translate to different languages

        if 'hindi' in lang.lower():
            to_lang = 'hi'
        elif 'french' in lang.lower():
            to_lang = 'fr'
        elif 'punjabi' in lang.lower():
            to_lang = 'pa'
        elif 'japanese' in lang.lower():
            to_lang = 'ja'

        # Creating a translator instance
        translator = Translator(to_lang)

        speak("Start speaking, we are translating as you speak !!")
        print("Start speaking, we are translating as you speak !!")
        
        while True:
            audio = recog.listen(source)
            try:
                lines = recog.recognize_google(audio)
                print("Here's what we heard :", lines)

                # Check if user wants to stop
                if 'stop' in lines.lower():
                    speak("Goodbye!")
                    break

                # Translating input to selected output language
                translated_lines = translator.translate(lines)
                speak(translated_lines)
                print(translated_lines)
            except spr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except spr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
