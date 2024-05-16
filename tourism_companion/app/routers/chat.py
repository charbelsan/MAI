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
# from app.services.pipeline import Pipeline
from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.config import Config
from app.chains import search_nearby, create_tourist_circuit, analyze_request, get_message
import os
import base64
import tempfile

import warnings
warnings.filterwarnings("ignore")

from langchain_core.prompts import PromptTemplate
from app.services.utils import play_mp3, get_circuits
from app.services.utils import setup_logging

# Set up logger
logger = setup_logging('logs/chat.log')

router = APIRouter()

# Load pipeline configurations
config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config/config.yaml")
# pipeline = Pipeline(config_file=config_file)  # Initialize the pipeline once

# Initialize OpenAI GPT-4 with the API key
openai_api_key = os.getenv("OPENAI_API_KEY")
gpt4_model = ChatOpenAI(model_name="gpt-4o", openai_api_key=Config.OPENAI_API_KEY, temperature=0.7)

# Define the prompt template for analyzing the user's request
template = """Question: {question}

Answer: You are an AI assistant that analyzes user requests to determine the appropriate action. Based on the user's input, you should categorize the request as one of the following: 'tourist_circuit' for creating a tourist circuit, 'find_nearby' for finding nearby places, or 'other' for any other type of request. Provide a clear and concise action flag based on your analysis."""

prompt = PromptTemplate.from_template(template)
llm_analyze_request = prompt | gpt4_model

# Load the RAG configuration
use_rag = False #pipeline.config['features'].get('use_rag', False)

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
    # session_id = start_or_get_session(db, request.user_id)
    # conversation_memory = get_conversation_memory(db, session_id)

    transcription = ""
    session_id = "1234"
    if request.text:
        play_mp3("start.mp3")
        transcription = request.text

        print("Transcription: ", transcription, type(transcription))
        logger.info(f"Transcription: {transcription}  {type(transcription)}")
        
        # Analyze the user's request to determine the appropriate action
        action_flag = llm_analyze_request.invoke(transcription).content
        print(f"Action Flag: {action_flag}")
        logger.info(f"Action Flag: {action_flag}")
        
        # # action_flag = analyze_request(transcription, conversation_memory)
        # action_flag = analyze_request(str(transcription))
        
        if "tourist_circuit" in action_flag:
            message_body = get_message()
            logger.info(f"Message body: {message_body}")
            path_csv = "benin_tourist_circuits.csv"
            if not os.path.exists(path_csv):
                path_csv = create_tourist_circuit(message_body, str(session_id))
            response = get_circuits(path_csv, only_circuit=True, circuit_name=None)
            play_mp3("stop.mp3")
            return {"response": response, "session_id": session_id}

        elif "find_nearby" in action_flag:
            if not request.gps_position:
                raise HTTPException(status_code=400, detail="GPS position is required for this request.")
            place_type = "restaurants" if "restaurants" in transcription else "hotels" if "hotels" in transcription else "tourist spots"
            logger.info(f"Place type: {place_type}")
            # response = search_nearby(request.gps_position, place_type, conversation_memory)
            response = action_flag
            play_mp3("stop.mp3")
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

