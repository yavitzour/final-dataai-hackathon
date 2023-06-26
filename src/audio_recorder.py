import pyaudio
from pynput import keyboard
import subprocess
import sys
import wave
#use 16Khz


FORMAT = 8
CHANNELS = 1
RATE = 44100 
CHUNK = 2048
RECORD_SECONDS = 5

ARECORD_POPEN = None

from .audio2text import audio_file_to_text
from .rest_api import client

def record_audio_arecord(ofile):
    global ARECORD_POPEN
    if ARECORD_POPEN is None:
        cmd = f"arecord -d 10 -f cd -t wav -D default {ofile}"
        ARECORD_POPEN = subprocess.Popen(cmd.split(" "))

def stop_recording(audio_file, log_file):
    global ARECORD_POPEN
    if ARECORD_POPEN is not None:
        subprocess.Popen.kill(ARECORD_POPEN)
        transcript = audio_file_to_text(audio_file)
        ARECORD_POPEN = None
        with open(log_file, 'a') as of:
            of.write(f"You: {transcript}\n")

        return transcript

"""
question = stop_recording("o.wav", "app.log")

answer = query_dolly(question, "app.log")
"""

def query_dolly(prompt, log_file):
    # query dolly
    answer = client.query_dolly(prompt) 

    with open(log_file, 'a') as lf:
        lf.write(f"Dolly: {answer}")

    return answer


def on_press(key):
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys

    if k == 'r':
        record_audio_arecord("o.wav")
    if k == 's':
       transcript = stop_recording("o.wav", "/tmp/app.log")
       print(f"transcript: {transcript}")

def main(argv):
    if len(argv) > 1 and argv[1] == "help":
        print(f"usage: {argv[0]} <wav_file_name>")
        print("example: python3 audio_recorder.py out.wav ")
        exit(0)

    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # start to listen on a separate thread
    listener.join()  # remove if main thread is polling self.keys


if __name__ == "__main__":
    main(sys.argv)

