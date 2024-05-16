import torch
import whisper
import torchaudio
import numpy as np
from transformers import AutoModelForSeq2SeqLM
from transformers import VitsModel, AutoTokenizer
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

import os
from app.services.utils import play_mp3

class WhisperInference:
    def __init__(self, model_name="base"):
        self.model = whisper.load_model(model_name)
        
    def inference(self, audio_file):
        result = self.model.transcribe(audio_file)
        return result['text']
        
class ASRInference:
    def __init__(self, model_name="chrisjay/fonxlsr"):
        self.model = Wav2Vec2ForCTC.from_pretrained(model_name)
        self.processor = Wav2Vec2Processor.from_pretrained(model_name)
    
    def inference(self, audio_file):
        audio_array, sample_rate = speech_file_to_array_fn(audio_file)
        inputs = self.processor(audio_array, sampling_rate=sample_rate, return_tensors="pt")
        with torch.no_grad():
            logits = self.model(**inputs).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        text = self.processor.decode(predicted_ids[0]).lower()
        return text
    
class TTSInference:
    def __init__(self, model_name="facebook/mms-tts-fon"):
        self.model = VitsModel.from_pretrained(model_name)
        self.processor = AutoTokenizer.from_pretrained(model_name)
    
    def inference(self, text, sample_rate=16000, audio_file=f"temp.wav"):
        inputs = self.processor(text, return_tensors="pt")
        with torch.no_grad():
            audio_array = self.model(**inputs).waveform
        torchaudio.save(audio_file, audio_array, sample_rate)
        return audio_array, audio_file
    
# Preprocessing the input.
# We need to read the audio files as arrays
def speech_file_to_array_fn(batch_path):
  speech_array, sampling_rate = torchaudio.load(batch_path)
  return speech_array.squeeze().numpy(), sampling_rate

if __name__ == '__main__':

    ## Call TTS Inference
    whisper = WhisperInference(model_name="base")
    asr = ASRInference(model_name="chrisjay/fonxlsr")
    tts = TTSInference(model_name="facebook/mms-tts-fon")

    list_text = [
        "Xɛ́, nɛ̌ wɛ a ka gbɔn, nɔví ce?",
        "mεɖe ɖu nu bɔ mεɖe ɔ nu sin",
        "tɔ ce xwe yɔyɔ din tɔn ɔ ci gblagadaa",
        "ṣùgbọ́n ọlọpáá alábòójútó ìhámọ́ lé",
        "áfíríkà nínú ìgbìmọ̀ ààbò àjọ",
    ]
    
    for fon_text in list_text:
                
        audio_array, audio_file = tts.inference(fon_text)
        print("TTS Audio Output : ", audio_file)

        print("FON text Input : ", fon_text)
        ## Call ASR Inference
        text_output = asr.inference(audio_file)
        print("Transcription from Audio - ASR : ", text_output)

        ## Translation Back
        text_output = whisper.inference(audio_file)
        print("Transcription from Audio - Whisper : ", text_output)
        print('#'*100)