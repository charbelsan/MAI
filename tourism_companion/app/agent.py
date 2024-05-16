from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain.memory import ConversationBufferMemory
from langchain_core.tools import Tool


from langchain_core.prompts import ChatPromptTemplate
from app.config import Config

# Initialize LLM
llm = OpenAI(model_name="gpt-4o", api_key=Config.OPENAI_API_KEY)

# Initialize Google Search tool
search = GoogleSearchAPIWrapper()

# Define the tool for Google Search
google_search_tool = Tool(
    name="google_search",
    description="Search Google for recent results.",
    func=search.run,
)


# Define the tools for the agents
tools = [google_search_tool]

# Initialize memory
memory = ConversationBufferMemory()

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

# Initialize nearby_agent with Google tools and prompt template
nearby_agent = initialize_agent(
    tools, llm, agent="zero-shot-react-description", prompt_template=prompt_template_nearby, verbose=True, memory=memory
)

# Initialize tourist_circuit_agent with Google tools and prompt template
tourist_circuit_agent = initialize_agent(
    tools, llm, agent="zero-shot-react-description", prompt_template=prompt_template_tourist_circuit, verbose=True, memory=memory
)

# Initialize analysis_agent without Google tools but with prompt template
analysis_agent = initialize_agent(
    tools, llm, agent="zero-shot-react-description", prompt_template=prompt_template_analysis, verbose=True, memory=memory
)

def search_nearby(location, place_type, conversation_memory):
    query = f"{place_type} near {location}"
    results = nearby_agent.run(input=query)
    return results

def create_tourist_circuit(location, conversation_memory):
    query = f"Create a tourist circuit near {location}"
    results = tourist_circuit_agent.run(input=query)
    return results

def analyze_request(request_text, conversation_memory):
    query = f"Analyze the following request: {request_text}"
    results = analysis_agent.run(input=query)
    return results
