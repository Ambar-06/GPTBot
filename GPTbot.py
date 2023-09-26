import pyttsx3 
import speech_recognition as sr
import requests


engine = pyttsx3.init('sapi5')

voices = engine.getProperty('voices')
print(voices)

engine.setProperty('voice' ,voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def listening():
    '''
        Will listen to the user and convert the audio to text
    '''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1  
        r.energy_threshold = 5000
        audio = r.listen(source)  

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")  
            print(f"User said: {query.capitalize()}")  
        except Exception:
            print("Couldn't recognize. Please say that again.")
            return "None"
    return query

def promptToGPT(query):
    url = "https://api.openai.com/v1/completions"
    # url = "https://api.openai.com/v1/chat/completions"
    access_key = ""
    org_token = ""
    header = {
        "content-type" : "application/json",
        "Authorization": f"Bearer {access_key}",
        "OpenAI-Organization": f"{org_token}"
    }
    prompt = {
     "model": "text-davinci-003",
     "prompt": f"User : {query}\n Mr.X :",
     "max_tokens": 70
    }
    # prompt = {
    #  "model": "gpt-3.5-turbo-base",
    #  "prompt": f"{query}",
    #  "max_tokens": 70
    # }
    prompt1 = {
    "model": "gpt-3.5-turbo-instruct",
    "prompt": f"{query}",
    "max_tokens": 70
    }
    data = requests.post(url, headers=header, json=prompt).json()
    return data['choices'][0]['text']


if __name__ == "__main__":
    while True:
        query = listening().lower()
        # query = input('Please enter something\n')
        ttt = promptToGPT(query)
        speak(ttt)
