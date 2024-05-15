from agent import create_nearby_agent, create_tourist_circuit_agent, create_analysis_agent
from langchain_core.memory import ConversationBufferMemory

def search_nearby(gps_position, place_type, conversation_memory: ConversationBufferMemory):
    """
    Use the agent to find nearby places based on GPS position and place type.

    Args:
        gps_position (dict): Dictionary containing latitude and longitude.
        place_type (str): Type of place to search for (e.g., restaurants, hotels).
        conversation_memory (ConversationBufferMemory): The conversation memory to use.

    Returns:
        str: The response from the agent.
    """
    input_text = f"Find {place_type} near latitude {gps_position['latitude']} and longitude {gps_position['longitude']}."
    agent = create_nearby_agent(conversation_memory)  # Use the provided conversation memory
    response = agent.run(input_text)
    return response

def create_tourist_circuit(gps_position, conversation_memory: ConversationBufferMemory):
    """
    Use the agent to create a tourist circuit based on GPS position.

    Args:
        gps_position (dict): Dictionary containing latitude and longitude.
        conversation_memory (ConversationBufferMemory): The conversation memory to use.

    Returns:
        str: The response from the agent.
    """
    input_text = f"Create a tourist circuit from latitude {gps_position['latitude']} and longitude {gps_position['longitude']}."
    agent = create_tourist_circuit_agent(conversation_memory)  # Use the provided conversation memory
    response = agent.run(input_text)
    return response

def analyze_request(request_text, conversation_memory: ConversationBufferMemory):
    """
    Use the agent to analyze the user's request and determine the appropriate action.

    Args:
        request_text (str): The user's request text.
        conversation_memory (ConversationBufferMemory): The conversation memory to use.

    Returns:
        str: The action flag ('tourist_circuit', 'find_nearby', or 'other').
    """
    input_text = f"Analyze the following request: {request_text}"
    agent = create_analysis_agent(conversation_memory)  # Use the provided conversation memory
    response = agent.run(input_text)
    return response
