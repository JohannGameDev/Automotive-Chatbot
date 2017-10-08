import speech_recognition as sr
import pydub
from pydub import AudioSegment
from os import path
import os


class SpeechToText(object):

    """docstring for SpeechToText."""
    def __init__(self):
        self.TELEGRAM_AUDIO_PATH = "telegram_audio/audio.ogg"
        self.CONVERTED_AUDIO_PATH = "telegram_audio/audio.wav"
        self.SERVICE = "google"
    def get_text_from_speech(self):
        try:
            print "Converting Audio from ogg to wav ..."
            AUDIO_FILE_OGG = path.join(path.dirname(path.realpath(__file__)), self.TELEGRAM_AUDIO_PATH)
            ogg_audio = AudioSegment.from_file(AUDIO_FILE_OGG, format="ogg")
            ogg_audio.export(self.CONVERTED_AUDIO_PATH,format="wav")
            AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), self.CONVERTED_AUDIO_PATH)
            # use the audio file as the audio source
            r = sr.Recognizer()
            with sr.AudioFile(AUDIO_FILE) as source:
                audio = r.record(source)  # read the entire audio file
            print "Recognize Text with service: " + self.SERVICE
            if self.SERVICE == "google":
                message = r.recognize_google(audio,language="de")
            if self.SERVICE == "wit":
                message = r.recognize_wit(audio, key=self.WIT_AI_KEY)
            print "You said: " + message
            return message

        except sr.UnknownValueError:
            print("Service could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from service; {0}".format(e))
            return None
