import datetime
import re
import requests
import sys
import webbrowser

import pyttsx3
import speech_recognition as sr
import wikipedia

from time import strftime
from pygooglenews import GoogleNews
from pyowm import OWM


def run_greeting():
    time = int(strftime('%H'))
    if 4 <= time < 12:
        say('Hello Sir, good morning')
    elif 12 <= time < 18:
        say('Hello Sir, good afternoon')
    else:
        say('Hello Sir, good evening')


def shutdown():
    say('Goodbye Sir, have a pleasant day')
    sys.exit()


def open_website(name):
    reg_ex = re.search('open (.+)', name)
    if reg_ex:
        domain = reg_ex.group(1)
        print(domain)
        url = 'https://www.' + domain + '.com'
        webbrowser.open(url)
        say('The website you have requested has been successfully opened for you, Sir')
    else:
        pass


def get_weather(city_phrase):
    reg_ex = re.search('weather in (.*)', city_phrase)
    if reg_ex:
        city = reg_ex.group(1)

        owm = OWM('ab0d5e80e8dafb2cb81fa9e82431c1fa')
        manager = owm.weather_manager()
        weather = manager.weather_at_place(city).weather

        status = weather.status
        detailed_status = weather.detailed_status
        temperature = weather.temperature('celsius')
        humidity = weather.humidity

        weather_report = 'Current weather in %s is %s (%s). The temperature is %0.1f degree Celsius,' \
                         ' feels like is %0.1f. The humidity is %s percents' % (
                             city, status, detailed_status, temperature['temp'], temperature['feels_like'], humidity)

        print(weather_report)
        say(weather_report)
    else:
        pass


def get_localtime():
    now = datetime.datetime.now()
    report = 'Current time is %d hours %d minutes' % (now.hour, now.minute)
    print(report)
    say(report)


def get_news(limit=4):
    try:
        google_news = GoogleNews().top_news()['entries']
        limit = limit if 0 <= limit <= len(google_news) else len(google_news)
        for news in google_news[:limit]:
            print(news['title'], '\n', news['link'])
            say(news['title'])
    except Exception as e:
        print(e)


def search_topic(topic_phrase):
    reg_ex = re.search('tell me about (.*)', topic_phrase)
    try:
        if reg_ex:
            topic = reg_ex.group(1)

            ny = wikipedia.page(topic)
            text = ny.summary[0:1000]

            print(text)
            say(text)
    except Exception as e:
        print(e)
        say(e)


def get_joke():
    res = requests.get(
        'https://icanhazdadjoke.com/',
        headers={"Accept": "application/json"})
    if res.status_code == requests.codes.ok:
        joke = str(res.json()['joke'])
        print(joke)
        say(joke)
    else:
        say('Oops! I ran out of jokes')


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
    if 'hello' in text_speech:
        run_greeting()
    elif 'shut down' in text_speech:
        shutdown()
    elif 'open' in text_speech:
        open_website(text_speech)
    elif 'weather in' in text_speech:
        get_weather(text_speech)
    elif 'time' in text_speech:
        get_localtime()
    elif 'news for today' in text_speech:
        get_news()
    elif 'joke' in text_speech:
        get_joke()
    elif 'tell me about' in text_speech:
        search_topic(text_speech)


while True:
    assistant(listen())
