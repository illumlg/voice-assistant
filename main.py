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

def get_news(limit):
    pass

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
    pass

def assistant(text_speech):
    pass