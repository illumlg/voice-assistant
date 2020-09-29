import re

import pyttsx3
import speech_recognition as sr
from pyowm import OWM

def run_greeting():
    pass

def shutdown():
    pass

def open_website(name):
    pass

def get_weather(cityPhrase):
    reg_ex = re.search('weather in (.*)', cityPhrase)
    if reg_ex:
        city = reg_ex.group(1)

        owm = OWM('ab0d5e80e8dafb2cb81fa9e82431c1fa')
        manager = owm.weather_manager()
        weather = manager.weather_at_place(city).weather

        status = weather.status
        detailedStatus = weather.detailed_status
        temperature = weather.temperature('celsius')
        humidity = weather.humidity

        weather_report = 'Current weather in %s is %s (%s). The temperature is %0.1f degree celcius,' \
                         ' feels like is %0.1f. The humidity is %s percents' % (
                             city, status, detailedStatus, temperature['temp'], temperature['feels_like'], humidity)

        print(weather_report)
        say(weather_report)


def get_localtime():
    pass

def get_news(limit):
    pass

def search_topic(topic):
    pass

def get_joke():
    pass

def listen():
    speech, r = '', sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=2)
        print('Say something...')
        audio = r.listen(source)
    try:
        speech = r.recognize_google(audio).lower()
        print('You said: ' + speech + '\n')
    except sr.UnknownValueError or sr.RequestError: print('....')
    finally: return speech

def say(text):
    engine = pyttsx3.init()
    engine.setProperty('voice', engine.getProperty('voices')[1].id)
    engine.setProperty('rate', 130)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def assistant(text_speech):
    pass