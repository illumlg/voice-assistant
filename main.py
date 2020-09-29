from pygooglenews import GoogleNews
import pyttsx3
import speech_recognition as sr
import re
import sys
import webbrowser
import datetime
from pyowm import OWM
from time import strftime


def run_greeting():
    time = int(strftime('%H'))
    if 4 <= time < 12:
        say('Hello Sir. Good morning')
    elif 12 <= time < 18:
        say('Hello Sir. Good afternoon')
    else:
        say('Hello Sir. Good evening')


def shutdown():
    say('Goodbye Sir. Have a pleasant day')
    sys.exit()


def open_website(name):
    reg_ex = re.search('open (.+)', name)
    if reg_ex:
        domain = reg_ex.group(1)
        print(domain)
        url = 'https://www.' + domain
        webbrowser.open(url)
        say('The website you have requested has been successfully opened for you, Sir.')
    else:
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
    else:
        pass


def get_localtime():
    now = datetime.datetime.now();
    say('Current time is %d hours %d minutes' % (now.hour, now.minute))


def get_news(limit=4):
    try:
        google_news = GoogleNews().top_news()['entries']
        limit = limit if 0 <= limit <= len(google_news) else len(google_news)
        for news in google_news[:limit]:
            print(news['title'],'\n',news['link'])
            say(news['title'])
    except Exception as e: print(e)


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
    except sr.UnknownValueError or sr.RequestError:
        print('....')
    finally:
        return speech


def say(text):
    engine = pyttsx3.init()
    engine.setProperty('voice', engine.getProperty('voices')[1].id)
    engine.setProperty('rate', 130)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def assistant(text_speech):
    pass
