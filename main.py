import re,datetime,requests,sys,webbrowser,pyttsx3,wikipedia
import speech_recognition as sr
from time import strftime
from pygooglenews import GoogleNews
from pyowm import OWM


def get_greeting():
    time = int(strftime('%H'))
    if 4 <= time < 12:
        print('Hello Sir, good morning')
        return 'Hello Sir, good morning'
    elif 12 <= time < 18:
        print('Hello Sir, good afternoon')
        return 'Hello Sir, good afternoon'
    else:
        print('Hello Sir, good evening')
        return 'Hello Sir, good evening'


def shutdown():
    print('Goodbye Sir, have a pleasant day')
    say('Goodbye Sir, have a pleasant day')
    sys.exit()


def open_website(name: str):
    reg_ex = re.search('open (.+)', name)
    try:
        domain = reg_ex.group(1)
        print(domain)
        url = 'https://www.' + domain + '.com'
        webbrowser.open(url)
    except Exception as e: print(e)


def get_weather(city_phrase: str)-> str:
    reg_ex = re.search('weather in (.*)', city_phrase)
    try:
        city = reg_ex.group(1)

        manager = OWM('ab0d5e80e8dafb2cb81fa9e82431c1fa').weather_manager()
        weather = manager.weather_at_place(city).weather

        status = weather.status
        detailed_status = weather.detailed_status
        temperature = weather.temperature('celsius')
        humidity = weather.humidity
        wind = weather.wind()['speed']

        weather_report = 'Current weather in %s is %s (%s).\n' \
                         'The temperature is %s degree Celsius, ' \
                         'feels like is %s.\nThe humidity is %s percents\n' \
                         'The wind is %s metres per second' % (
                             city, status, detailed_status, int(temperature['temp']),
                             int(temperature['feels_like']), int(humidity), int(wind))

        print(weather_report)
        return weather_report
    except Exception as e: print(e)


def get_localtime()-> str:
    now = datetime.datetime.now()
    time_report = 'Current time is {}h {}m'.format(now.hour, now.minute)
    print(time_report)
    return time_report


def get_news(limit=4)-> list:
    try:
        google_news = GoogleNews().top_news()['entries']
        limit = limit if 0 <= limit <= len(google_news) else len(google_news)
        return google_news[:limit]
    except Exception as e: print(e)


def search_topic(topic_phrase: str, sentences=4)-> str:
    reg_ex = re.search('tell me about (.*)', topic_phrase)
    try:
        topic = reg_ex.group(1)
        text = wikipedia.summary(topic, sentences=sentences)
        print(text)
        return text
    except Exception as e: print(e)


def get_joke()-> str:
    try:
        res = requests.get(
            'https://icanhazdadjoke.com/',
            headers={"Accept": "application/json"})
        if res.status_code == requests.codes.ok:
            joke = res.json()['joke']
            print(joke)
            return joke
        else: return 'Oops! I ran out of jokes'
    except Exception as e: print(e)


def listen()-> str:
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


def say(text: str):
    engine = pyttsx3.init()
    engine.setProperty('voice', engine.getProperty('voices')[1].id)
    engine.setProperty('rate', 130)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def assistant(text_speech: str):
    if 'hello' in text_speech:
        say(get_greeting())
    elif 'shut down' in text_speech:
        shutdown()
    elif 'open' in text_speech:
        open_website(text_speech)
        say('The website you have requested has been successfully opened for you Sir')
    elif 'weather in' in text_speech:
        weather_report = get_weather(text_speech)
        say(weather_report)
    elif 'time' in text_speech:
        time = get_localtime()
        say(time)
    elif 'news for today' in text_speech:
        news_lst = get_news()
        for news in news_lst:
            print(news['title'], '\n', news['link'])
            say(news['title'])
    elif 'joke' in text_speech:
        joke = get_joke()
        say(joke)
    elif 'tell me about' in text_speech:
        text = search_topic(text_speech)
        say(text)

while True:
    assistant(listen())