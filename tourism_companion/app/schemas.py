from pydantic import BaseModel, Field, validator
from typing import Optional, Dict

class ChatRequest(BaseModel):
    text: Optional[str] = Field(None, description="User's text input")
    file: Optional[bytes] = Field(None, description="Audio file input in bytes")
    image: Optional[bytes] = Field(None, description="Image file input in bytes")
    gps_position: Optional[Dict[str, float]] = Field(None, description="GPS coordinates (latitude, longitude)")
    place_type: Optional[str] = Field(None, description="Type of place to search for (e.g., restaurants, hotels)")
    user_id: int = Field(..., description="User's ID")
    target_lang: str = Field(..., description="Target language for translation")

    @validator('gps_position')
    def validate_gps_position(cls, v):
        if v is not None and ('latitude' not in v or 'longitude' not in v):
            raise ValueError('GPS position must include latitude and longitude')
        return v

class ChatResponse(BaseModel):
    response: str = Field(..., description="AI's response to the user's query")
    session_id: int = Field(..., description="Session ID for the conversation")

class SpeechToTextRequest(BaseModel):
    audio: str = Field(..., description="Base64 encoded audio file")
    inputLang: str = Field(..., description="Input language for the audio")

class SpeechToTextResponse(BaseModel):
    text: str = Field(..., description="Transcribed text from the audio")

class TextToSpeechRequest(BaseModel):
    text: str = Field(..., description="Text to convert to speech")
    inputLang: str = Field(..., description="Input language of the text")
    outputLang: str = Field(..., description="Output language for the audio")

class TextToSpeechResponse(BaseModel):
    audio: str = Field(..., description="Base64 encoded audio file")
