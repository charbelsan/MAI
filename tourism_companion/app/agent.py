from langchain.agents import Agent
from langchain_community.llms import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from app.tool import GoogleSearchTool
from app.config import Config

# Define the prompt template for finding nearby places
prompt_template_nearby = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI assistant specializing in helping users find nearby places based on their GPS location. You are provided with the user's location (latitude and longitude) and the type of place they are looking for (e.g., restaurants, hotels, tourist attractions). Use this information to provide accurate and relevant suggestions for nearby places."
        ),
        ("human", "{input}"),
    ]
)

# Define the prompt template for creating a tourist circuit
prompt_template_tourist_circuit = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI assistant specializing in creating tourist circuits based on the user's current GPS position. Given the user's location (latitude and longitude), create a logical sequence of tourist spots that are interesting and worth visiting. Consider the proximity of locations and provide a detailed itinerary with multiple stops for the user to follow."
        ),
        ("human", "{input}"),
    ]
)

# Define the prompt template for analyzing the user's request
prompt_template_analysis = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI assistant that analyzes user requests to determine the appropriate action. Based on the user's input, you should categorize the request as one of the following: 'tourist_circuit' for creating a tourist circuit, 'find_nearby' for finding nearby places, or 'other' for any other type of request. Provide a clear and concise action flag based on your analysis."
        ),
        ("human", "{input}"),
    ]
)

# Initialize OpenAI GPT-4
llm = OpenAI(model_name="gpt-4o", openai_api_key=Config.OPENAI_API_KEY)

def create_agent(memory, template, search_function=None):
    """
    Create an agent with a given memory, prompt template, and optional search function.

    Args:
        memory (ConversationBufferMemory): The memory to use with the agent.
        template (ChatPromptTemplate): The prompt template to use with the agent.
        search_function (function, optional): The search function to use with the agent.

    Returns:
        Agent: The created agent.
    """
    agent = Agent(
        llm=llm,
        prompt_template=template,
        memory=memory
    )

    if search_function:
        agent.tools['google_search'] = GoogleSearchTool

    return agent

def create_nearby_agent(memory):
    """
    Create an agent for finding nearby places.

    Args:
        memory (ConversationBufferMemory): The memory to use with the agent.

    Returns:
        Agent: The created agent for finding nearby places.
    """
    return create_agent(memory, prompt_template_nearby, lambda query: google_search(query, Config.GOOGLE_API_KEY, Config.GOOGLE_CSE_ID))

def create_tourist_circuit_agent(memory):
    """
    Create an agent for creating tourist circuits.

    Args:
        memory (ConversationBufferMemory): The memory to use with the agent.

    Returns:
        Agent: The created agent for creating tourist circuits.
    """
    return create_agent(memory, prompt_template_tourist_circuit, lambda query: google_search(query, Config.GOOGLE_API_KEY, Config.GOOGLE_CSE_ID))

def create_analysis_agent(memory):
    """
    Create an agent for analyzing user requests.

    Args:
        memory (ConversationBufferMemory): The memory to use with the agent.

    Returns:
        Agent: The created agent for analyzing user requests.
    """
    return create_agent(memory, prompt_template_analysis)