
# For managing audio file
import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

#arecord -d 10 -f cd -t wav -D copy foobar.wav


def main():
    tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

    audio, rate = librosa.load("data/example.wav", sr=16000)
    print(audio)
    print(rate)

    input_values = tokenizer(audio, return_tensors="pt").input_values
    logits = model(input_values).logits
    prediction = torch.argmax(logits, dim=-1)
    transcription = tokenizer.batch_decode(prediction)[0]
    print(transcription)

    pass

if __name__ == '__main__':
    main()