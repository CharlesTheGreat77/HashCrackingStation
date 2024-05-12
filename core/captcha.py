import subprocess, requests
import speech_recognition as sr
from typing import Optional

def ffmpeg_converter(url: str) -> bool:
    '''
    function to convert the audio captcha to wav file format using ffmpeg & deletes the now old mp3
    '''
    try:
        request = requests.get(url)

        with open('mp3_captcha.mp3', 'wb') as file:
            file.write(request.content)

        wav_converter = 'ffmpeg -i mp3_captcha.mp3 captcha.wav -loglevel quiet'
        subprocess.run(wav_converter, shell=True)
        remove_file = 'rm -rf mp3_captcha.mp3'
        subprocess.run(remove_file, shell=True)
        return True
    except Exception as err:
        print(f"[-] Error downloading and converting audio: {err}")
        return False

def speech_to_text(audio_file: str) -> Optional[str]:
    '''
    function to do audio to text with googles speech recognition using the SpeechRecognition lib
    returns captcha
    '''
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)
        captcha = r.recognize_google(audio)
        remove_file = 'rm -rf captcha.wav'
        subprocess.run(remove_file, shell=True)

        return captcha

    except sr.UnknownValueError as err:
        print(f"[-] Error reading audio: {err}")
        return None
    except Exception as err:
        print(f"[-] Unknown Error occurred: {err}")
        return None # return None if error occured