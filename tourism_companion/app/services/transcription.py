import whisper
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

# Initialize models for Yoruba
whisper_model_yoruba = whisper.load_model("base")

# Initialize models for Fon
wav2vec2_model_fon = Wav2Vec2ForCTC.from_pretrained("chrisjay/fonxlsr")
wav2vec2_processor_fon = Wav2Vec2Processor.from_pretrained("chrisjay/fonxlsr")

def transcribe_audio(file: bytes, language: str) -> str:
    if language == "yo":
        result = whisper_model_yoruba.transcribe(file)
        return result['text']
    elif language == "fon":
        inputs = wav2vec2_processor_fon(file, return_tensors="pt", padding=True)
        with torch.no_grad():
            logits = wav2vec2_model_fon(**inputs).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = wav2vec2_processor_fon.batch_decode(predicted_ids)
        return transcription[0]
    else:
        raise ValueError("Unsupported language for transcription")
