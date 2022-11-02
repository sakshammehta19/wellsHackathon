import requests
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import speech_recognition as s_r
from simplejson import JSONDecodeError

# server url
URL = "http://localhost:5000/customer_query"


# audio file we'd like to send for predicting keyword
FILE_PATH = "recording.wav"


if __name__ == "__main__":
    r = s_r.Recognizer()
    my_mic = s_r.Microphone(device_index=1)    
    with my_mic as source:
        print("Say now!!!!")
        r.adjust_for_ambient_noise(source) #reduce noise
        audio = r.listen(source) #take voice input from the microphone
        with open(FILE_PATH,'wb') as f:
            f.write(audio.get_wav_data())

    file = open(FILE_PATH, "rb")
    values = {"file": (FILE_PATH, file, "audio/wav")}
    response = requests.post(URL, files=values)
    try:
        data = response.json()
        print(data)
        usecase = str(data["usecase"])
        print("Predicted sentiment: {}".format(data["sentiment"]))

        if str(data["usecase"]) == "None":
            print("Please be more specific with your query.")
        else:
            print("Thank you, your query has been recieved and assigned to {}".format(data["usecase"])+" team.")
    except:
        print("Try again")
    