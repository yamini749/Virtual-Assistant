import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import time
import requests
import webbrowser

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            print('Listening...')
            talk("Hi, what can I do for you?")
            voice = listener.listen(source, timeout=5)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except sr.UnknownValueError:
        print("Sorry, I didn't get that. Please repeat.")
        talk("Sorry, I didn't get that. Please repeat.")
    except sr.RequestError:
        print("Network error.")
        talk("There seems to be a network error.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return command

def run_alexa():
    command = take_command()
    print(command)

    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)

    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        print(current_time)
        talk('Current time is ' + current_time)

    elif 'who is the' in command:
        person = command.replace('who is the ', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)

    elif 'weather' in command:
        city = command.replace('weather in ', '')
        talk(f'Getting the weather information for {city}')
        weather_info = get_weather(city)
        if weather_info:
            talk(weather_info)
        else:
            talk('Unable to fetch weather information at the moment.')

    elif 'reminder' in command:
        reminder = command.replace('reminder ', '')
        talk(f'Reminder set: {reminder}')
        print(f'Reminder: {reminder}')

    elif 'open website' in command:
        site = command.replace('open website ', '')
        url = f"https://{site.strip()}"
        talk(f'Opening {site}')
        webbrowser.open(url)

    elif 'calculate' in command:
        result = evaluate_expression(command.replace('calculate', '').strip())
        if result is not None:
            talk(f'The result is {result}')
            print(f'The result is {result}')
        else:
            talk('Sorry, I cannot perform this calculation.')

    elif 'joke' in command:
        res = pyjokes.get_joke()
        print(res)
        talk(res)

    elif 'are you single' in command:
        talk('I am in a relationship with wifi')
    elif 'bye' in command or 'goodbye' in command:
        talk('Goodbye!')
        return False  # Stop the loop
    else:
        talk("Please say the command again, because I didn't quite catch that.")
    time.sleep(2)
    return True

def get_weather(city):
    try:
        api_key = "15524be7ab27c13196b2e61ab78c2681"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        if data["cod"] != "404":
            main = data["main"]
            temperature = main["temp"]
            weather_description = data["weather"][0]["description"]
            weather_info = f'The temperature in {city} is {temperature} degrees Celsius with {weather_description}.'
            return weather_info
        else:
            return "City not found."
    except Exception as e:
        print(f"An error occurred while fetching weather: {e}")
        return None

def evaluate_expression(expression):
    try:
        result = eval(expression)
        return result
    except Exception as e:
        print(f"Error evaluating expression: {e}")
        return None
while True:
    if not run_alexa():
        break
