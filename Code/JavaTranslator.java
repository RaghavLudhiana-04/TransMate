import java.io.File;
import java.io.IOException;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.Clip;
import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.UnsupportedAudioFileException;
import java.util.Scanner;
import java.util.concurrent.TimeUnit;

import com.darkprograms.speech.microphone.Microphone;
import com.darkprograms.speech.recognizer.GoogleResponse;
import com.darkprograms.speech.recognizer.Recognizer;
import com.darkprograms.speech.recognizer.Recognizer.Languages;
import com.darkprograms.speech.synthesiser.Synthesiser;
import com.darkprograms.speech.util.Gender;

public class SpeechTranslation {
    public static void main(String[] args) {
        Synthesiser synthesiser = new Synthesiser("Microsoft Server Speech Text to Speech Voice (en-US, Jessa24KRUS)");
        Microphone microphone = new Microphone(FLACFileWriter.FLAC);

        try {
            System.out.println("Say Hello to initiate the conversation !!");
            synthesiser.speakText("Say Hello to initiate the conversation !!", Gender.FEMALE, "en-US");

            System.out.println("Listening...");
            System.out.println();

            while (true) {
                try {
                    microphone.open();
                    TimeUnit.SECONDS.sleep(5);
                    microphone.captureAudioToFile("speech.wav");

                    TimeUnit.SECONDS.sleep(5); // Delay for recording

                    microphone.close();

                    Recognizer recognizer = new Recognizer(Languages.ENGLISH_US);
                    GoogleResponse response = recognizer.getRecognizedDataForWave("speech.wav");

                    String text = response.getResponse();

                    System.out.println(text);

                    if (text.toLowerCase().contains("hello")) {
                        System.out.println("\nGot you!!!\n");

                        System.out.println("Kindly Choose a Language from below");
                        System.out.println("Hindi \nFrench \nGujarati \nJapanese");

                        microphone.open();
                        TimeUnit.SECONDS.sleep(5);
                        microphone.captureAudioToFile("lang.wav");

                        TimeUnit.SECONDS.sleep(5); // Delay for recording

                        microphone.close();

                        response = recognizer.getRecognizedDataForWave("lang.wav");
                        String lang = response.getResponse();

                        System.out.println(lang);
                        System.out.println();

                        String toLang = "en";

                        if (lang.toLowerCase().contains("hindi")) {
                            toLang = "hi";
                        } else if (lang.toLowerCase().contains("french")) {
                            toLang = "fr";
                        } else if (lang.toLowerCase().contains("gujarati")) {
                            toLang = "gu";
                        } else if (lang.toLowerCase().contains("japanese")) {
                            toLang = "ja";
                        }

                        Translator translator = Translator.getInstance();
                        translator.setSourceLanguage("en");
                        translator.setTargetLanguage(toLang);

                        System.out.println("Start speaking, we are translating as you speak !!");
                        synthesiser.speakText("Start speaking, we are translating as you speak !!", Gender.FEMALE,
                                "en-US");

                        microphone.open();
                        TimeUnit.SECONDS.sleep(5);

                        while (true) {
                            microphone.captureAudioToFile("translate.wav");

                            TimeUnit.SECONDS.sleep(5); // Delay for recording

                            microphone.close();

                            response = recognizer.getRecognizedDataForWave("translate.wav");
                            String lines = response.getResponse();

                            System.out.println("Here's what I heard: " + lines);

                            if (lines.toLowerCase().contains("stop")) {
                                synthesiser.speakText("Goodbye!", Gender.FEMALE, "en-US");
                                break;
                            }

                            String translatedLines = translator.translate(lines);

                            System.out.println("Translated speech: " + translatedLines);

                            synthesiser.speakText(translatedLines, Gender.FEMALE, toLang);
                        }
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                    synthesiser.speakText("An error occurred. Please try again.", Gender.FEMALE, "en-US");
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
