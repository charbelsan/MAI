from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.schemas import SpeechToTextRequest, SpeechToTextResponse
from app.services.pipeline import Pipeline
from app.services.utils import play_mp3
import base64
import tempfile
import os

import warnings
warnings.filterwarnings("ignore")

router = APIRouter()

# Load pipeline configurations
config_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config/config.yaml")
pipeline = Pipeline(config_file=config_file)  # Initialize the pipeline once

@router.post("/speechToText", response_model=SpeechToTextResponse)
async def speech_to_text(request: SpeechToTextRequest):
    """
    Convert speech (audio file) to text.

    Args:
        request (SpeechToTextRequest): The request payload containing the audio file in base64 and input language.

    Returns:
        SpeechToTextResponse: JSON response containing the transcribed text.
    """
    audio_base64 = request.audio
    input_lang = request.inputLang
    
    print("audio_base64 ", audio_base64)

    play_mp3("start.mp3")
    if not audio_base64 or not input_lang:
        raise HTTPException(status_code=400, detail="Audio file and input language are required")

    # Decode base64 audio file
    # audio_bytes = base64.b64decode(audio_base64)
    # audio_bytes = base64.b64decode(audio_base64.encode('utf-8'))
    audio_bytes = audio_base64.encode('utf-8')
    
    # Save to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio_file:
        temp_audio_file.write(audio_bytes)
        temp_audio_file_path = temp_audio_file.name
    
    # Perform transcription
    transcription = pipeline.pipeline_att(audio_file=temp_audio_file_path, language=input_lang)
    
    print("Transcription: ", transcription)
    play_mp3("stop.mp3")
    # # Clean up temporary file
    # os.remove(temp_audio_file_path)
    
    return SpeechToTextResponse(text=transcription)
