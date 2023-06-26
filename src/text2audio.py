'''
sudo apt install espeak
pip install pyttsx3
'''

import pyttsx3
voice = 'english_rp+m1'


def text_to_speech(sentence):
    engine = pyttsx3.init()
    #voice = engine.getProperty('voices')
    #engine.setProperty('voice', voice[11].id)
    engine.setProperty('voice', voice) 
    engine.say(sentence)
    engine.runAndWait()

if __name__ == '__main__':
    text_to_speech("Hi! I'm dolly")
