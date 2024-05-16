from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.schemas import TextToSpeechRequest, TextToSpeechResponse
from app.services.pipeline import Pipeline
from app.services.utils import play_mp3
import base64
import os

import warnings
warnings.filterwarnings("ignore")

router = APIRouter()

# Load pipeline configurations
config_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config/config.yaml")
pipeline = Pipeline(config_file=config_file)  # Initialize the pipeline once

@router.post("/textToSpeech", response_model=TextToSpeechResponse)
async def text_to_speech(request: TextToSpeechRequest):
    """
    Convert text to speech (audio file).

    Args:
        request (TextToSpeechRequest): The request payload containing the text and input/output languages.

    Returns:
        TextToSpeechResponse: JSON response containing the base64 encoded audio file.
    """
    text = request.text
    input_lang = request.inputLang
    output_lang = request.outputLang

    play_mp3("start.mp3")
    if not text or not input_lang or not output_lang:
        raise HTTPException(status_code=400, detail="Text, input language, and output language are required")

    # Perform text-to-speech conversion
    audio_file_path = pipeline.pipeline_ta(text=text, language=output_lang)
    
    # Read the audio file and encode to base64
    with open(audio_file_path, "rb") as audio_file:
        audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")
    
    print("Play audio ", audio_file_path)
    play_mp3(audio_file_path)
    play_mp3("stop.mp3")
    # # Clean up temporary file
    # os.remove(audio_file_path)
    
    return TextToSpeechResponse(audio=audio_base64)
