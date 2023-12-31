from flask import Flask, render_template, request, jsonify, send_file
from src.audio_recorder import *
from src.text2audio import *
from src.rest_api.client import DollyClient

app = Flask(__name__)

HOST = "ec2-18-218-57-116.us-east-2.compute.amazonaws.com"
PORT = 80
WAVE_OUTPUT_FILENAME = "/tmp/output.wav"
TEXT_FILE_PATH = "/tmp/chatlog.txt"

client = DollyClient(HOST, PORT)
#client.init_client()

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
    response = query_llm(client, transcript, TEXT_FILE_PATH)
    text_to_speech(response)
    return jsonify({'message': 'Recording stopped'})


@app.route('/get_text', methods=['GET'])
def get_text():
    output = read_text_file()
    return output

if __name__ == '__main__':
    app.run()
