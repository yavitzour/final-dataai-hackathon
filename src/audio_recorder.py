import pyaudio
import sys
import wave
#use 16Khz


FORMAT = 8
CHANNELS = 1
RATE =  1600
CHUNK = 1024
RECORD_SECONDS = 5

def record_audio(device, file, recording_seconds):
    with wave.open(file, 'wb') as wf:
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,\
                        frames_per_buffer=CHUNK, input_device_index=int(device))
        frames = []

        for _ in range(0, int(RATE / CHUNK * recording_seconds)):
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()
        
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))


def main(argv):
    if argv[1] == "help":
        print(f"usage: {argv[0]} <device_idx> <wav_file_name> <length of recording in seconds>")
        print("example: python3 audio_recorder.py 12 out.wav 5")
        exit(0)

    device = argv[1]
    wav_file = argv[2]
    recording_seconds = int(argv[3])

    record_audio(device, wav_file, recording_seconds)

if __name__ == "__main__":
    main(sys.argv)

