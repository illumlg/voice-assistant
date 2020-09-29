from pygooglenews import GoogleNews
import pyttsx3
import speech_recognition as sr


def run_greeting():
    pass

def shutdown():
    pass

def open_website(name):
    pass

def get_weather(city):
    pass

def get_localtime():
    pass

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
    speech,r = '', sr.Recognizer()
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