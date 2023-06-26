from flask import Flask, render_template, request, jsonify, send_file
import wave
import threading
#import pyttsx3
from src.audio_recorder import *
from src.text2audio import *

app = Flask(__name__)

WAVE_OUTPUT_FILENAME = "/tmp/output.wav"
TEXT_FILE_PATH = "/tmp/chatlog.txt"

def read_text_file():
    try:
        output = subprocess.check_output(['tail', '-n', '100', TEXT_FILE_PATH], universal_newlines=True)
    except subprocess.CalledProcessError:
        output = ''

    return output

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_recording', methods=['POST'])
def _start_recording():
    record_audio_arecord(WAVE_OUTPUT_FILENAME)
    return jsonify({'message': 'Recording started'})

@app.route('/stop_recording', methods=['POST'])
def _stop_recording():
    transcript = stop_recording(WAVE_OUTPUT_FILENAME, TEXT_FILE_PATH)
    text_to_speech(transcript)
    return jsonify({'message': 'Recording stopped'})


@app.route('/play', methods=['GET'])
def play():
    wave_file = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wave_file.getsampwidth()),
                    channels=wave_file.getnchannels(),
                    rate=wave_file.getframerate(),
                    output=True)

    data = wave_file.readframes(CHUNK)

    while data:
        stream.write(data)
        data = wave_file.readframes(CHUNK)

    stream.stop_stream()
    stream.close()
    p.terminate()

    return 'Audio playback finished!'

@app.route('/get_text', methods=['GET'])
def get_text():
    output = read_text_file()
    return output

@app.route('/get_audio', methods=['GET'])
def get_audio():
    return send_file(WAVE_OUTPUT_FILENAME, as_attachment=True, attachment_filename=WAVE_OUTPUT_FILENAME)

if __name__ == '__main__':
    app.run()
