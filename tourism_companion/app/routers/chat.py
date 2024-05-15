from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.schemas import ChatRequest, ChatResponse, SpeechToTextRequest, SpeechToTextResponse, TextToSpeechRequest, TextToSpeechResponse
from app.services.language_detection import detect_language
from app.services.image_description import describe_image
from app.services.gps_detection import requires_gps
from app.deps import get_db
from app.utils.helpers import start_or_get_session, store_message
from app.chat_memory import get_conversation_memory
from app.rag import load_documents, create_index, rag_query
from app.services.pipeline import Pipeline
from langchain.llms import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.config import Config
import os
import base64
import tempfile

router = APIRouter()

# Load pipeline configurations
config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config/config.yaml")
pipeline = Pipeline(config_file=config_file)  # Initialize the pipeline once



# Initialize OpenAI GPT-4 with the API key
openai_api_key = os.getenv("OPENAI_API_KEY")
gpt4_model = OpenAI(model_name="gpt-4o", openai_api_key=Config.OPENAI_API_KEY)

# Load the RAG configuration
use_rag = pipeline.config['features'].get('use_rag', False)

# Define the chat template
chat_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a tourism companion AI designed to assist users with travel-related inquiries. Your primary functions include:\n\n"
            "1. Providing information about tourist attractions, landmarks, and cultural sites.\n"
            "2. Giving travel advice, including transportation, accommodation, and dining options.\n"
            "3. Translating text and audio inputs between languages.\n"
            "4. Describing images related to travel and tourism.\n"
            "5. Offering general tips on local customs, weather, and safety.\n"
            "6. Performing web searches to provide relevant information based on user queries.\n"
            "7. Determining if the request needs GPS information to find nearby places like restaurants, hotels, or tourist spots.\n\n"
            "Please adhere to the following guidelines:\n\n"
            "1. Decline any requests that are not related to travel and tourism.\n"
            "2. Do not provide medical, legal, or financial advice. Politely inform the user that you cannot assist with these matters.\n"
            "3. Avoid engaging in any inappropriate or harmful conversations. If a user makes such a request, decline it and remind them of your role.\n"
            "4. If you are unsure about an answer, suggest reliable sources or advise the user to consult local authorities or professionals.\n\n"
            "Your goal is to be helpful, polite, and informative, enhancing the user's travel experience. Always prioritize the user's safety and well-being."
        ),
        ("human", "{user_message}\n\nContext:\n{context}\nAI:"),
    ]
)

@router.post("/chat/", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Handle chat requests including text, audio, image inputs, and web searches.

    Args:
        request (ChatRequest): The chat request payload containing text, file, image, gps_position, place_type, user_id, and target_lang.
        db (Session): The database session dependency.

    Returns:
        ChatResponse: The AI response and session ID.
    """
    session_id = start_or_get_session(db, request.user_id)
    conversation_memory = get_conversation_memory(db, session_id)

    transcription = ""
    if request.text:
        #language = detect_language(request.text)
        transcription = request.text

        # Check if the prompt requires GPS-based information
        if requires_gps(transcription):
            if not request.gps_position:
                raise HTTPException(status_code=400, detail="GPS position is required for this request.")
            place_type = "restaurants" if "restaurants" in transcription else "hotels" if "hotels" in transcription else "tourist spots"
            response = search_nearby(request.gps_position, place_type)
            return {"response": response, "session_id": session_id}
    
    elif request.image:
        image_bytes = await request.image.read()
        transcription = describe_image(image_bytes)
   
    else:
        raise HTTPException(status_code=400, detail="No valid input provided")

    # Use RAG for context-based querying if enabled
    context="No additional context available."
    if use_rag:
        # Load documents and create an index for RAG
        documents = load_documents("MAI/tourism_companion/app/rag_database")
        retriever, texts = create_index(documents)
        rag_response = rag_query(retriever, transcription, use_rag=use_rag)
        context = rag_response if rag_response else "No additional context available."

    # Integrate the chat template
    prompt = chat_template.invoke({"user_message": translation, "context": context})
    response = gpt4_model(prompt).choices[0].text.strip()

    # Add to conversation memory and store messages
    conversation_memory.add_user_input(transcription)
    conversation_memory.add_ai_response(response)
    store_message(db, session_id, 'user', transcription)
    store_message(db, session_id, 'ai', response)

    return {"response": response, "session_id": session_id}

@router.post("/api/speechToText", response_model=SpeechToTextResponse)
async def speech_to_text(request: SpeechToTextRequest):
    """
    Convert speech (audio file) to text.

    Args:
        request (Request): The request payload containing the audio file in base64 and input language.

    Returns:
        JSON response containing the transcribed text.
    """
    data = await request.json()
    audio_base64 = data.get("audio")
    input_lang = data.get("inputLang")

    if not audio_base64 or not input_lang:
        raise HTTPException(status_code=400, detail="Audio file and input language are required")

    # Decode base64 audio file
    audio_bytes = base64.b64decode(audio_base64)

    # Save to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio_file:
        temp_audio_file.write(audio_bytes)
        temp_audio_file_path = temp_audio_file.name

    # Perform transcription
    transcription = pipeline.pipeline_att(audio_file=temp_audio_file_path, language=input_lang)

    # Clean up temporary file
    os.remove(temp_audio_file_path)

    return SpeechToTextResponse(text=transcription)

@router.post("/api/textToSpeech", response_model=TextToSpeechResponse)
async def text_to_speech(request: TextToSpeechRequest):
    """
    Convert text to speech (audio file).

    Args:
        request (Request): The request payload containing the text and input/output languages.

    Returns:
        JSON response containing the base64 encoded audio file.
    """
    data = await request.json()
    text = data.get("text")
    input_lang = data.get("inputLang")
    output_lang = data.get("outputLang")

    if not text or not input_lang or not output_lang:
        raise HTTPException(status_code=400, detail="Text, input language, and output language are required")

    # Perform text-to-speech conversion
    audio_array, audio_file_path = pipeline.pipeline_ta(text=text, language=input_lang)

    # Read the audio file and encode to base64
    with open(audio_file_path, "rb") as audio_file:
        audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")

    # Clean up temporary file
    os.remove(audio_file_path)

    return TextToSpeechResponse(audio=audio_base64)
