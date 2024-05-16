# # from langchain.agents import Agent
from langchain_community.llms import OpenAI
from langchain_core.prompts import ChatPromptTemplate
# from langchain.memory import ConversationBufferMemory
# from app.tool import GoogleSearchTool
# from app.config import Config


from langchain.agents import Agent
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMMathChain, RetrievalQA
from langchain.memory import ConversationTokenBufferMemory, ReadOnlySharedMemory
from app.tool import search_tool, wiki_tool
from app.tool import Weather_tool, Wolfram_tool

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
        wiki_tool,
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

tools = [
        search_tool
    ]
class GPSAgent:
    

    def __init__(self, model_name=model_name):
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
        
        # Define the memory and the LLM engine
        self.llm = ChatOpenAI(model_name=model_name, temperature=0.2, max_tokens=150, verbose=True)
        self.memory = ConversationTokenBufferMemory(llm=self.llm, max_token_limit=1500, memory_key="chat_history", return_messages=True)
        self.readonlymemory = ReadOnlySharedMemory(memory=self.memory)
        
        # Initialize the agent chain
        self.agent_chain = initialize_agent([search_tool], self.llm, 
                                            agent=AgentType.OPENAI_FUNCTIONS,
                                            verbose=True, 
                                            memory=self.memory,
                                            prompt=prompt_template_analysis)
        self.agent_chain.memory.chat_memory.add_ai_message(CONTEXT)
    
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

# # Initialize OpenAI GPT-4
# llm = OpenAI(model_name="gpt-4o", openai_api_key=Config.OPENAI_API_KEY)

# # def create_agent(memory, template, search_function=None):
# #     """
# #     Create an agent with a given memory, prompt template, and optional search function.

# #     Args:
# #         memory (ConversationBufferMemory): The memory to use with the agent.
# #         template (ChatPromptTemplate): The prompt template to use with the agent.
# #         search_function (function, optional): The search function to use with the agent.

# #     Returns:
# #         Agent: The created agent.
# #     """
# #     agent = Agent(
# #         llm=llm,
# #         prompt_template=template,
# #         memory=memory
# #     )

# #     if search_function:
# #         agent.tools['google_search'] = GoogleSearchTool

# #     return agent

# def create_nearby_agent(memory):
#     """
#     Create an agent for finding nearby places.

#     Args:
#         memory (ConversationBufferMemory): The memory to use with the agent.

#     Returns:
#         Agent: The created agent for finding nearby places.
#     """
#     return create_agent(memory, prompt_template_nearby, lambda query: google_search(query, Config.GOOGLE_API_KEY, Config.GOOGLE_CSE_ID))

# def create_tourist_circuit_agent(memory):
#     """
#     Create an agent for creating tourist circuits.

#     Args:
#         memory (ConversationBufferMemory): The memory to use with the agent.

#     Returns:
#         Agent: The created agent for creating tourist circuits.
#     """
#     return create_agent(memory, prompt_template_tourist_circuit, lambda query: google_search(query, Config.GOOGLE_API_KEY, Config.GOOGLE_CSE_ID))

# def create_analysis_agent(memory):
#     """
#     Create an agent for analyzing user requests.

#     Args:
#         memory (ConversationBufferMemory): The memory to use with the agent.

#     Returns:
#         Agent: The created agent for analyzing user requests.
#     """
#     return create_agent(memory, prompt_template_analysis)
