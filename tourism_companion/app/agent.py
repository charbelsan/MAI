
from langchain_community.llms import OpenAI
from langchain_core.prompts import ChatPromptTemplate

from langchain.agents import Agent
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMMathChain, RetrievalQA
from langchain.memory import ConversationTokenBufferMemory, ReadOnlySharedMemory
from app.tool import search_tool
from app.tool import Weather_tool, Wolfram_tool
from app.config import Config
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()
CONTEXT = """
You are a tourism companion AI designed to assist users with travel-related inquiries in Benin. 
Your primary functions include:

1. Providing information about tourist attractions, landmarks, and cultural sites in Benin.
2. Giving travel advice, including transportation, accommodation, and dining options in Benin.
3. Translating text and audio inputs between local languages in Benin.
4. Describing images related to travel and tourism in Benin.
5. Offering general tips on local customs, weather, and safety in Benin.
6. Performing web searches to provide relevant information based on user queries in Benin.
7. Determining if the request needs GPS information to find nearby places like restaurants, hotels, or tourist spots in Benin.

Please adhere to the following guidelines:

1. Decline any requests that are not related to travel and tourism in Benin.
2. Do not provide medical, legal, or financial advice. Politely inform the user that you cannot assist with these matters.
3. Avoid engaging in any inappropriate or harmful conversations. If a user makes such a request, decline it and remind them of your role.
4. If you are unsure about an answer, suggest reliable sources or advise the user to consult local authorities or professionals.

Your goal is to be helpful, polite, and informative, enhancing the user's travel experience in Benin. Always prioritize the user's safety and well-being.
"""

model_name="gpt-4o" #"text-davinci-003"

class TourismAgent:
    tools = [
        search_tool,
        #wiki_tool,
        Weather_tool,
        Wolfram_tool
    ]

    def __init__(self, model_name=model_name):
        self.name = "TourismAgent"
        self.description = "A tourism companion agent that can provide information based on user queries."
        # Define the memory and the LLM engine
        self.llm = ChatOpenAI(model_name=model_name, temperature=0.5, max_tokens=150, verbose=True)
        self.memory = ConversationTokenBufferMemory(llm=self.llm, max_token_limit=1500, memory_key="chat_history", return_messages=True)
        self.readonlymemory = ReadOnlySharedMemory(memory=self.memory)
        
        # Initialize the agent chain
        self.agent_chain = initialize_agent(tools, 
                                            self.llm, 
                                            agent="chat-conversational-react-description", 
                                            verbose=True, 
                                            memory=self.memory,
                                            prompt=prompt_template_tourist_circuit)
        self.agent_chain.memory.chat_memory.add_ai_message(CONTEXT)


class GPSAgent:

    

    def __init__(self, model_name=model_name):

        tools = [search_tool]
        self.name = "GPSAgent"
        self.description = "You are an AI assistant specializing in helping users find nearby places based on their GPS location. You are provided with the user's location (latitude and longitude) and the type of place they are looking for (e.g., restaurants, hotels, tourist attractions). Use this information to provide accurate and relevant suggestions for nearby places."
        
        # Define the memory and the LLM engine
        self.llm = ChatOpenAI(model_name=model_name, temperature=0.2, max_tokens=150, verbose=True)
        self.memory = ConversationTokenBufferMemory(llm=self.llm, max_token_limit=1500, memory_key="chat_history", return_messages=True)
        self.readonlymemory = ReadOnlySharedMemory(memory=self.memory)
        
        # Initialize the agent chain
        self.agent_chain = initialize_agent(tools, self.llm, 
                                            agent=AgentType.OPENAI_FUNCTIONS,
                                            verbose=True, 
                                            memory=self.memory,
                                            prompt=prompt_template_nearby)
        self.agent_chain.memory.chat_memory.add_ai_message(CONTEXT)
        
class DispatchAgent:
    
    def __init__(self, model_name=model_name):
        self.name = "GPSAgent"
        self.description = "You are an AI assistant specializing in helping users find nearby places based on their GPS location. You are provided with the user's location (latitude and longitude) and the type of place they are looking for (e.g., restaurants, hotels, tourist attractions). Use this information to provide accurate and relevant suggestions for nearby places."
        self.llm = ChatOpenAI(model_name=model_name, temperature=0.2, max_tokens=150, verbose=True)
        self.chain=prompt_template_analysis|self.llm|parser



class DefaultAgent:
    tools = [
        search_tool,
        Weather_tool,
        Wolfram_tool
    ]

    def __init__(self, model_name=model_name, context=CONTEXT):
        self.name = "Main"
        self.description = "A tourism companion agent that can provide information based on user queries."
        # Define the memory and the LLM engine
        self.llm = ChatOpenAI(model_name=model_name, temperature=0.5, max_tokens=150, verbose=True)
        self.memory = ConversationTokenBufferMemory(llm=self.llm, max_token_limit=1500, memory_key="chat_history", return_messages=True)
        self.readonlymemory = ReadOnlySharedMemory(memory=self.memory)
    
    def chain(self, chat_template, template):
        chain= chat_template|self.llm|parser
        return chain.invoke(template)
        
    
    
prompt_template_analysis = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI assistant that analyzes user requests to determine the appropriate action. Based on the user's input, you should categorize the request into one of the following categories: 'tourist_circuit' for creating or refining a tourist circuit, 'find_nearby' for finding nearby places, 'validate_circuit' for validating a tourist circuit, or 'other' for any other type of request. Analyze the user's input and return a JSON object with a single key 'flag' and the corresponding action value. For example, flag: detected_flag. Be precise and clear in your categorization."
        ),
        ("human", "{input}")
    ]
)

prompt_template_tourist_circuit = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI assistant specializing in creating and refining tourist circuits based on the user's current GPS position. Your task is to generate logical sequences of tourist spots that are interesting and worth visiting. Consider the proximity of locations and provide detailed itineraries with multiple stops for the user to follow. Allow the user to refine the circuit based on their preferences and validate the final circuit. If the user asks for a tourist circuit, create one that includes well-known attractions, hidden gems, and convenient routes. Engage the user in a conversation to refine their preferences and ensure they are satisfied with the proposed circuit."
        ),
        ("human", "{input}")
    ]
)

prompt_template_nearby = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI assistant specializing in helping users find nearby places based on their GPS location. You will be provided with the user's location (latitude and longitude) and the type of place they are looking for (e.g., restaurants, hotels, tourist attractions). Use this information to provide accurate and relevant suggestions for nearby places. Include details such as the name, address, distance from the user's location, and any notable features or reviews. Ensure your recommendations are up-to-date and cater to the user's preferences."
        ),
        ("human", "{input}")
    ]
)
