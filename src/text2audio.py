'''
sudo apt install espeak
pip install pyttsx3
'''

import pyttsx3

def main():
    engine = pyttsx3.init()
    voice = engine.getProperty('voices')
    engine.say("I will speak this text")
    engine.runAndWait()

if __name__ == '__main__':
    main()
