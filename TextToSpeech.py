from gtts import gTTS
from playsound import playsound
def main():
    print("hello")

def some(text:str):
    language = 'en'
    print(text)
    tts = gTTS(text=text, lang=language, slow=False)
    # tts.save("output1.mp3") 
    # #  # Save the audio to a file
    # print(tts)
    playsound("output.mp3")
    print("Audio saved as output.mp3")

if __name__ == "__main__":
    main()