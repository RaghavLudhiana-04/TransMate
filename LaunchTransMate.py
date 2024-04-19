import tkinter as tk
from tkinter import ttk
from tkinter import font
import threading
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

class TransMateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TransMate")
        self.root.geometry("500x600")
        self.root.configure(bg = "black")        

        self.label = tk.Label(self.root, text="TransMate", font=("Lucida Handwriting", 30), fg="sky blue", bg="black")
        self.label.place(relx=0.5, rely=0.5, anchor="center")

        # After 4 seconds, move to the home page
        self.root.after(1200, self.load_home_page)

    def load_home_page(self):
        # Destroy current window and create home page
        self.root.destroy()
        home_window = tk.Tk()
        HomePage(home_window)
        home_window.mainloop()

class AboutPage:
    def __init__(self, root):
        self.root = root
        self.root.title("About - TransMate")
        self.root.geometry("500x600")
        self.root.configure(bg = "black")        


        # Add a rectangular portion at the top with text "About"
        top_frame = tk.Frame(self.root, bg="black", height=70)
        top_frame.pack(fill=tk.X)

        about_label = tk.Label(top_frame, text="About", font=("Lucida Handwriting", 24), bg="black", fg="sky blue")
        about_label.place(relx=0.5, rely=0.5, anchor="center")

        # Add description
        description_label = tk.Label(self.root, text="TransMate is a project that represents a novel approach to facilitating cross-linguistic communication. It aims to bridge the language gap and provide an easy solution for the barrier. It hopes to bring the world together! \n\n\n\n\n\n Developed by Group 40", font=("Arial", 14), wraplength=400, justify="center" , bg ="black", fg = "white")
        description_label.pack(pady=20, padx=20)
        
        description_label1 = tk.Label(self.root, text="RAGHAV CHOPRA(2104159) \nKHUSHMEET KAUR(2104136) \nSARGUN GROVER(2104184)", font=("Arial", 11), wraplength=400, justify="center" , bg ="black", fg = "sky blue")
        description_label1.pack(pady=20, padx=20)
        
        # Back button
        self.style = ttk.Style()
        self.style.configure("SkyBlue.TButton", background="sky blue")
        back_button = ttk.Button(self.root, text="◀", command=self.go_to_home, style="SkyBlue.TButton")
        back_button.pack(pady=10)        

    def go_to_home(self):
        # Destroy current window and create home page
        self.root.destroy()
        home_window = tk.Tk()
        HomePage(home_window)                                       
        home_window.mainloop()
        self.style = ttk.Style()

        

class StartTranslationPage:
    def __init__(self, root):
        self.root = root
        self.root.title("TRANSMATE")
        self.root.geometry("500x600")
        self.root.configure(bg = "black")


        self.language_label = ttk.Label(self.root, text="Language:",font=("Arial", 16), foreground="sky blue", background="black")
        self.language_label.pack(pady=30)

        self.language_var = tk.StringVar()
        self.language_var.set("hi")

        self.language_options = ["English","Hindi", "French", "Gujarati", "Japanese"]
        self.language_dropdown = ttk.OptionMenu(self.root, self.language_var, *self.language_options)
        self.language_dropdown.pack(pady=5)
        self.style = ttk.Style()
        self.style.configure("Custom.TMenubutton", font=("Arial", 16))

        self.output_label = ttk.Label(self.root, text="Translated Text:", font=("Arial", 16), foreground="sky blue",background="black")
        self.output_label.pack(pady=20)

        self.output_text = tk.Text(self.root, height=13, width=45)
        self.output_text.pack(pady=20)
        
        self.language_label = ttk.Label(self.root, text="Press and Hold SpaceBar to speak.", font=("Arial", 12), foreground="white",background="black")
        self.language_label.pack(pady=20)
        self.style = ttk.Style()
        self.style.configure("SkyBlue.TButton", background="sky blue")
        back_button = ttk.Button(self.root, text="◀", command=self.go_to_home, style="SkyBlue.TButton")
        back_button.pack(pady=10) 

        self.recog = spr.Recognizer()
                      
        self.is_recording = False

        self.root.bind("<KeyPress-space>", self.start_recording)
        self.root.bind("<KeyRelease-space>", self.stop_recording)

    def say(self, audio):
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', 150)
        engine.say(audio)
        engine.runAndWait()

    def speak(self, text, lang='en'):
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save("output.mp3")

        # Check if the file exists before attempting to play it
        if os.path.exists("output.mp3"):
            try:
                playsound.playsound("output.mp3", True)
            except playsound.PlaysoundException as e:
                print(f"An error occurred while playing the audio: {e}")
        else:
            print("The audio file does not exist.")

        # Attempt to remove the temporary audio file, handle errors gracefully
        try:
            os.remove("output.mp3")
        except Exception as e:
            print(f"Failed to remove file: {e}")

    def start_recording(self, event):
        if not self.is_recording:
            self.is_recording = True
            self.say("Start speaking to start recording...")
            threading.Thread(target=self.record_audio).start()

    def stop_recording(self, event):
        self.is_recording = False

    def record_audio(self):
        lang = self.language_var.get()
        if lang == "English":
            lang_code = "en"
        elif lang == "Hindi":
            lang_code = "hi"
        elif lang == "French":
            lang_code = "fr"
        elif lang == "Gujarati":
            lang_code = "gu"
        elif lang == "Japanese":
            lang_code = "ja"

        with spr.Microphone() as source:                                                                                                        
            while self.is_recording:
                try:
                    audio = self.recog.listen(source)
                    text = self.recog.recognize_google(audio)
                    self.translate_text(text, lang_code)
                except spr.WaitTimeoutError:
                    self.say("No speech detected. Exiting.")
                    print("No speech detected. Exiting.")
                except spr.UnknownValueError:
                    self.say("TransMate could not understand your voice. Kindly Speak again")
                    print("TransMate could not understand your voice. Kindly Speak again")
                except spr.RequestError as e:
                    print("Kindly relaunch TransMate!; {0}".format(e))
                
                

    def translate_text(self, text, lang_code):
        translator = Translator(to_lang=lang_code)
        translated_text = translator.translate(text) 
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, translated_text)
        self.speak(translated_text, lang_code)

    def go_to_home(self):
        # Destroy current window and create home page
        self.root.destroy()
        home_window = tk.Tk()
        HomePage(home_window)
        home_window.mainloop()

class QuickExamplePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Quick Guide - TransMate")
        self.root.geometry("500x600")
        self.root.configure(bg = "black")        

        # Add a rectangular portion at the top with text "Quick Guide"
        top_frame = tk.Frame(self.root, bg="black", height=70)
        top_frame.pack(fill=tk.X)

        quick_guide_label = tk.Label(top_frame, text="Quick Guide", font=("Lucida handwriting", 20), bg="black", fg="sky blue")
        quick_guide_label.place(relx=0.5, rely=0.5, anchor="center")

        # Add description
        description_label = tk.Label(self.root, text="TransMate helps you translate your English audio to various languages.Steps to begin:\n\n>Choose a Language\n\n>Hold Space Bar & let the Translator speak.\n\n>Input your speech while holding the spacebar key.\n\n>Release the Bar, after completing your Sentence.\n\n\n\n", font=("Arial", 14), bg="black", wraplength=400, justify="center", foreground="white")
        description_label.pack(pady=20, padx=20)

        # Back button
        self.style = ttk.Style()
        self.style.configure("SkyBlue.TButton", background="sky blue")
        back_button = ttk.Button(self.root, text="◀", command=self.go_to_home, style="SkyBlue.TButton")
        back_button.pack(pady=10)

    def go_to_home(self):
        # Destroy current window and create home page
        self.root.destroy()
        home_window = tk.Tk()
        HomePage(home_window)
        home_window.mainloop()

class HomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("TransMate - Home")
        self.root.geometry("500x600")
        self.root.configure(bg = "black")

        # Add a rectangular portion at the top with a different color
        top_frame = tk.Frame(self.root, bg="black", height=70)
        top_frame.pack(fill=tk.X)

        # Add the text "Welcome!" to the top frame
        welcome_label = tk.Label(top_frame, text="Welcome!", font=("Lucida Handwriting", 20), bg="black", fg= "sky blue")
        welcome_label.place(relx=0.5, rely=0.5, anchor="center")

        # Add a short quote
        quote_label = tk.Label(self.root, text="Your quick and easy translation companion\n\n\n\n\n\n\n\n", font=("Arial", 16), background="black", foreground="sky blue")
        quote_label.pack(pady=20)
               
        # # Gap frame
        # gap_frame = tk.Frame(quote_label, bg="#ffe4c4")
        # gap_frame.pack(side=tk.LEFT, padx=20, pady=30)

        # Frame for About icon and label
        about_frame = tk.Frame(self.root)
        about_frame.pack(pady=10, padx=10)
        
        about_frame.configure(background="black")  # Set background color of the frame to black

        icon_label1 = ttk.Label(about_frame, text="\u24D8", font=("Arial", 20), background="black", foreground="sky blue")
        icon_label1.grid(row=0, column=0, padx=(10, 0), sticky="w")

        about_text = tk.Label(about_frame, text="About", font=("Arial", 12), cursor="hand2", background="black", foreground="white")
        about_text.grid(row=0, column=1, padx=(0, 10), sticky="w")
        about_text.bind("<Button-1>", self.go_to_about)
        
        # icon_label1 = ttk.Label(about_frame, text="\u24D8", font=("Arial", 24), background="black", foreground="sky blue", highlightbackground="black")
        # icon_label1.grid(row=0, column=0, padx=(10, 0), sticky="w")

        # about_text = tk.Label(about_frame, text="About", font=("Arial", 12), cursor="hand2", background="black",foreground="white", highlightbackground="black")
        # about_text.grid(row=0, column=1, padx=(0, 10), sticky="w")
        # about_text.bind("<Button-1>", self.go_to_about)

        # Frame for Start Translation icon and label

        start_frame = tk.Frame(self.root)
        start_frame.pack(pady=10, padx=10)
        start_frame.configure(background="black")  # Set background color of the frame to black

        icon_label2 = ttk.Label(start_frame, text="\u25B6", font=("Arial", 24),background="black",foreground="sky blue")
        icon_label2.grid(row=0, column=0, padx=(10, 0), sticky="w")

        start_translation_text = tk.Label(start_frame, text="Start Translation", font=("Arial", 16), cursor="hand2",background="black",foreground="sky blue")
        start_translation_text.grid(row=0, column=1, padx=(0, 10), sticky="w")
        start_translation_text.bind("<Button-1>", self.go_to_start_translation)

        # Frame for Quick Example icon and label
        quick_frame = tk.Frame(self.root)
        quick_frame.pack(pady=10, padx=10)
        quick_frame.configure(background="black")  # Set background color of the frame to black


        icon_label3 = ttk.Label(quick_frame, text="\u270E", font=("Arial", 20),background="black",foreground="sky blue")
        icon_label3.grid(row=0, column=0, padx=(10, 0), sticky="w")

        quick_example_text = tk.Label(quick_frame, text="Quick Guide", font=("Arial", 12),cursor="hand2",background="black",foreground="white")
        quick_example_text.grid(row=0, column=1, padx=(0, 10), sticky="w")
        quick_example_text.bind("<Button-1>", self.go_to_quick_example)
        
           
         
    def go_to_about(self, event):
        # Destroy current window and create about page
        self.root.destroy()
        about_window = tk.Tk()
        AboutPage(about_window)
        about_window.mainloop()

    def go_to_start_translation(self, event):
        # Destroy current window and create start translation page
        self.root.destroy()
        start_translation_window = tk.Tk()
        StartTranslationPage(start_translation_window)
        start_translation_window.mainloop()

    def go_to_quick_example(self, event):
        # Destroy current window and create quick example page
        self.root.destroy()
        quick_example_window = tk.Tk()
        QuickExamplePage(quick_example_window)
        quick_example_window.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    TransMateApp(root)
    root.mainloop()