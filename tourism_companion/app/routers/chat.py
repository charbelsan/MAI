from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import ChatRequest, ChatResponse
from app.services.language_detection import detect_language
from app.services.transcription import transcribe_audio
from app.services.translation import translate_text
from app.services.image_description import describe_image
from app.services.gps_detection import requires_gps
from app.deps import get_db
from app.utils.helpers import start_or_get_session, store_message
from app.chat_memory import get_conversation_memory
from app.rag import load_documents, create_retriever, create_compression_retriever, rag_query
from app.chains import search_nearby
from app.chains import search_nearby
from app.agent import tourism_agent
from langchain.llms import OpenAI

router = APIRouter()

# Load documents and create an index for RAG
documents = load_documents("path_to_your_pdf_directory")
index, texts = create_index(documents)

# Initialize OpenAI GPT-4
gpt4_model = OpenAI(model_name="text-davinci-003")

# Define the pre-prompt
pre_prompt = """
You are a tourism companion AI designed to assist users with travel-related inquiries. Your primary functions include:

1. Providing information about tourist attractions, landmarks, and cultural sites.
2. Giving travel advice, including transportation, accommodation, and dining options.
3. Translating text and audio inputs between languages.
4. Describing images related to travel and tourism.
5. Offering general tips on local customs, weather, and safety.
6. Performing web searches to provide relevant information based on user queries.
7. Determining if the request needs GPS information to find nearby places like restaurants, hotels, or tourist spots.

Please adhere to the following guidelines:

1. Decline any requests that are not related to travel and tourism.
2. Do not provide medical, legal, or financial advice. Politely inform the user that you cannot assist with these matters.
3. Avoid engaging in any inappropriate or harmful conversations. If a user makes such a request, decline it and remind them of your role.
4. If you are unsure about an answer, suggest reliable sources or advise the user to consult local authorities or professionals.

Your goal is to be helpful, polite, and informative, enhancing the user's travel experience. Always prioritize the user's safety and well-being.
"""

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
    language = ""
    if request.text:
        language = detect_language(request.text)
        transcription = request.text
        
        # Check if the prompt requires GPS-based information
        if requires_gps(transcription):
            if not request.gps_position:
                raise HTTPException(status_code=400, detail="GPS position is required for this request.")
            place_type = "restaurants" if "restaurants" in transcription else "hotels" if "hotels" in transcription else "tourist spots"
            response = search_nearby(request.gps_position, place_type)
            return {"response": response, "session_id": session_id}
    elif request.file:
        file_bytes = await request.file.read()
        language = detect_language(file_bytes)
        transcription = transcribe_audio(file_bytes, language)
    elif request.image:
        image_bytes = await request.image.read()
        transcription = describe_image(image_bytes)
    elif request.gps_position and request.place_type:
        # Handle GPS-based search
        response = search_nearby(request.gps_position, request.place_type)
        return {"response": response, "session_id": session_id}
    else:
        raise HTTPException(status_code=400, detail="No valid input provided")

    translation = translate_text(transcription, language, request.target_lang)
    
    # Use RAG for context-based querying
    rag_response = rag_query(index, texts, transcription)
    
    # Integrate the pre-prompt
    prompt = f"{pre_prompt}\n\nUser: {translation}\n\nContext:\n{rag_response}\nAI:"
    response = gpt4_model(prompt).choices[0].text.strip()

    # Add to conversation memory and store messages
    conversation_memory.add_user_input(transcription)
    conversation_memory.add_ai_response(response)
    store_message(db, session_id, 'user', transcription)
    store_message(db, session_id, 'ai', response)

    return {"response": response, "session_id": session_id}
