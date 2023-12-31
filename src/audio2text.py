
# For managing audio file
import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer


tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")


def audio_file_to_text(ifile):
    
    audio, rate = librosa.load(ifile, sr=16000)

    input_values = tokenizer(audio, return_tensors="pt").input_values
    logits = model(input_values).logits
    prediction = torch.argmax(logits, dim=-1)
    transcription = tokenizer.batch_decode(prediction)[0]
    return transcription


if __name__ == '__main__':
    print(audio_file_to_text("/tmp/o.wav"))
