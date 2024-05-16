import os
import re
import time
import shelve
import logging
import subprocess
#import pandas as pd
from dotenv import load_dotenv
# from langchain_community.llms import OpenAI
from openai import OpenAI

# from app.agent import create_nearby_agent, create_analysis_agent
from app.agent import DispatchAgent, GPSAgent, TourismAgent,DefaultAgent
# from langchain_core.memory import ConversationBufferMemory
from langchain.memory import ConversationBufferMemory

# Initialize the agent chain
dispatch_agent = DispatchAgent("gpt-4o")
gps_agent = GPSAgent("gpt-4o").agent_chain
main_agent_1=DefaultAgent("gpt-4o")

                
# Get the current file path
app_path = os.path.dirname(os.path.abspath(__file__))

# Initialize OpenAI GPT-4
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")
client = OpenAI(api_key=OPENAI_API_KEY)



def main_chain(translation , context, chat_template):
    template={"user_message": translation, "context": context}
    main_agent_1.chain(chat_template,template)



def search_nearby(gps_position, place_type, conversation_memory: ConversationBufferMemory=None):
    """
    Use the agent to find nearby places based on GPS position and place type.

    Args:
        gps_position (dict): Dictionary containing latitude and longitude.
        place_type (str): Type of place to search for (e.g., restaurants, hotels).
        conversation_memory (ConversationBufferMemory): The conversation memory to use.

    Returns:
        str: The response from the agent.
    """
    input_text = f"Find {place_type} near latitude {gps_position['lat']} and longitude {gps_position['lng']}."
    #gps_agent.memory.chat_memory.add_user_message(input_text)
    response = gps_agent.run(input=input_text)
    return response

def create_tourist_circuit(message_body, user_id="1234"): #, conversation_memory: ConversationBufferMemory):
    """
    Use the agent to create a tourist circuit based on GPS position.

    Args:
        gps_position (dict): Dictionary containing latitude and longitude.
        conversation_memory (ConversationBufferMemory): The conversation memory to use.

    Returns:
        str: The response from the agent.
    """
    
    # Check if there is already a thread_id for the user_id
    thread_id = check_if_thread_exists(user_id)

    # If a thread doesn't exist, create one and store it
    if thread_id is None:
        logging.info(f"Creating new thread with user_id {user_id}")
        thread = client.beta.threads.create()
        store_thread(user_id, thread.id)
        thread_id = thread.id
        
    # Otherwise, retrieve the existing thread
    else:
        logging.info(f"Retrieving existing thread with user_id {user_id}")
        thread = client.beta.threads.retrieve(thread_id)

    # Add message to thread
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_body,
    )

    # Run the assistant and get the new message
    new_message = run_assistant(thread)
    
    python_code = extract_python_code(new_message)
    save_to_file(f"{app_path}/benin_map.py", python_code)
    command = f"python3 {app_path}/benin_map.py"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return "benin_tourist_circuits.csv"

def analyze_request(request_text):
    """
    Use the agent to analyze the user's request and determine the appropriatgit e action.

    Args:
        request_text (str): The user's request text.

    Returns:
        str: The action flag ('tourist_circuit', 'find_nearby', or 'other').
    """
    return dispatch_agent.chain.invoke({"input": request_text})



def run_assistant(thread):
    # Retrieve the Assistant
    logging.info(f"Retrieving assistant : OPENAI_ASSISTANT_ID")
    assistant = client.beta.assistants.retrieve("asst_TFxNTT43nimozOZllIsEQV6X")

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions=f"You are a tourism companion AI designed to assist users with travel-related inquiries in Benin.",
    )

    # Wait for completion
    # https://platform.openai.com/docs/assistants/how-it-works/runs-and-run-steps#:~:text=under%20failed_at.-,Polling%20for%20updates,-In%20order%20to
    while run.status != "completed":
        # Be nice to the API
        # time.sleep(2)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # Retrieve the Messages
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    new_message = messages.data[0].content[0].text.value
    logging.info(f"Generated message: {new_message}")
    return new_message

message_body = "Make a list of places to discover for a vacation in all regions of Benin? \
    Groups a few places in the form of a tourist circuit of less than 5 places by generating the GPS coordinates \
        in a python dictionary list of this format: [{'id': 1, 'name': Cotono Dantokpa Market, 'description': \
            'One of the largest markets in West Africa, offering everything from fresh produce to traditional crafts \
                and textiles', 'latitude': 6.3671, 'longitude' : 2.4335}, {'id': 2, 'name': Fidjrosse Beach, \
                    'description': 'A beautiful sandy beach perfect for relaxation, swimming, and enjoying local seafood', \
                        'latitude': 6.3650, 'longitude': 2.3758} ] \
                            Offer me 5 different tourist circuits with the possibility of reusing the same places in different circuits\
                                \
        Collect and represent these circuits on a map of Benin with different colors in python. \
        connect places on the same circuit by a line \
        save the Coordinates as an dataframe file with columns: (circuit, id, name, description, latitude, longitude) on benin_tourist_circuits.csv\
        save the map as an HTML file named benin_tourist_circuits.html \
        use this template for the code : \
        '''\
        import folium \
        from folium import plugins \
        # Coordinates for different circuits  \
        TODO Add there the coordinates of the circuits \
        # Create a folium map centered around a central point in Benin \
        map_benin = folium.Map(location=[9.3077, 2.3158], zoom_start=7) \
        # Function to add a circuit to the map with a specified color and create a feature group for each circuit \
        def add_circuit_to_map(circuit_list, color, name): \
            feature_group = folium.FeatureGroup(name=name) \
            locations = [] \
            for place in circuit_list: \
                folium.Marker( \
                    location=[place['latitude'], place['longitude']], \
                    popup=place['nom'], \
                    icon=folium.Icon(color=color) \
                ).add_to(feature_group) \
                locations.append((place['latitude'], place['longitude'])) \
            folium.PolyLine(locations, color=color, weight=2.5, opacity=1).add_to(feature_group) \
            feature_group.add_to(map_benin) \
        # Add circuits to the map with different colors \
        add_circuit_to_map(historical_circuit, 'red', 'Historical and Cultural Heritage') \
        add_circuit_to_map(beach_circuit, 'blue', 'Coastal and Beach Relaxation') \
        add_circuit_to_map(nature_circuit, 'green', 'Natural Wonders and Safari') \
        add_circuit_to_map(artistic_circuit, 'purple', 'Artistic and Educational Trip') \
        add_circuit_to_map(adventure_circuit, 'orange', 'Adventure and Exploration') \
        # Add layer control to the map \
        folium.LayerControl().add_to(map_benin) \
        # Save the map to an HTML file \
        map_benin.save('benin_tourist_circuits.html') \
        ''' "

def create_tourist_circuit(message_body=message_body, user_id="1234"): #, conversation_memory: ConversationBufferMemory):
    """
    Use the agent to create a tourist circuit based on GPS position.

    Args:
        gps_position (dict): Dictionary containing latitude and longitude.
        conversation_memory (ConversationBufferMemory): The conversation memory to use.

    Returns:
        str: The response from the agent.
    """
    
    # Check if there is already a thread_id for the user_id
    thread_id = check_if_thread_exists(user_id)

    # If a thread doesn't exist, create one and store it
    if thread_id is None:
        logging.info(f"Creating new thread with user_id {user_id}")
        thread = client.beta.threads.create()
        store_thread(user_id, thread.id)
        thread_id = thread.id
        
    # Otherwise, retrieve the existing thread
    else:
        logging.info(f"Retrieving existing thread with user_id {user_id}")
        thread = client.beta.threads.retrieve(thread_id)

    # Add message to thread
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_body,
    )

    # Run the assistant and get the new message
    new_message = run_assistant(thread)
    
    python_code = extract_python_code(new_message)
    save_to_file(f"{app_path}/benin_map.py", python_code)
    command = f"python3 {app_path}/benin_map.py"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return "benin_tourist_circuits.csv"

def analyze_request(request_text):
    print(request_text)
    """
    Use the agent to analyze the user's request and determine the appropriatgit e action.

    Args:
        request_text (str): The user's request text.

    Returns:
        str: The action flag ('tourist_circuit', 'find_nearby', or 'other').
    """
    return dispatch_agent.chain.invoke({"input": request_text})


        
def get_message():
    return message_body
                    
# Use context manager to ensure the shelf file is closed properly
def check_if_thread_exists(user_id):
    with shelve.open(f"threads_db_benin") as threads_shelf:
        return threads_shelf.get(user_id, None)

def store_thread(user_id, thread_id):
    with shelve.open(f"threads_db_benin", writeback=True) as threads_shelf:
        threads_shelf[user_id] = thread_id

def extract_python_code(gpt_response):
    # Regular expression pattern to match Python code blocks
    pattern = r'```python(.*?)```'
    code_blocks = re.findall(pattern, gpt_response, re.DOTALL)
    return '\n\n'.join(code_blocks)

def save_to_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)
    

if __name__ == '__main__':
    
    message_body = "Make a list of places to discover for a vacation in all regions of Benin? \
    Groups a few places in the form of a tourist circuit of less than 5 places by generating the GPS coordinates \
        in a python dictionary list of this format: [{'id': 1, 'name': Cotono Dantokpa Market, 'description': \
            'One of the largest markets in West Africa, offering everything from fresh produce to traditional crafts \
                and textiles', 'latitude': 6.3671, 'longitude' : 2.4335}, {'id': 2, 'name': Fidjrosse Beach, \
                    'description': 'A beautiful sandy beach perfect for relaxation, swimming, and enjoying local seafood', \
                        'latitude': 6.3650, 'longitude': 2.3758} ] \
                            Offer me 5 different tourist circuits with the possibility of reusing the same places in different circuits\
                                \
        Collect and represent these circuits on a map of Benin with different colors in python. \
        connect places on the same circuit by a line \
        save the Coordinates as an dataframe file with columns: (circuit, id, name, description, latitude, longitude) on benin_tourist_circuits.csv\
        save the map as an HTML file named benin_tourist_circuits.html \
        use this template for the code : \
        '''\
        import folium \
        from folium import plugins \
        # Coordinates for different circuits  \
        TODO Add there the coordinates of the circuits \
        # Create a folium map centered around a central point in Benin \
        map_benin = folium.Map(location=[9.3077, 2.3158], zoom_start=7) \
        # Function to add a circuit to the map with a specified color and create a feature group for each circuit \
        def add_circuit_to_map(circuit_list, color, name): \
            feature_group = folium.FeatureGroup(name=name) \
            locations = [] \
            for place in circuit_list: \
                folium.Marker( \
                    location=[place['latitude'], place['longitude']], \
                    popup=place['nom'], \
                    icon=folium.Icon(color=color) \
                ).add_to(feature_group) \
                locations.append((place['latitude'], place['longitude'])) \
            folium.PolyLine(locations, color=color, weight=2.5, opacity=1).add_to(feature_group) \
            feature_group.add_to(map_benin) \
        # Add circuits to the map with different colors \
        add_circuit_to_map(historical_circuit, 'red', 'Historical and Cultural Heritage') \
        add_circuit_to_map(beach_circuit, 'blue', 'Coastal and Beach Relaxation') \
        add_circuit_to_map(nature_circuit, 'green', 'Natural Wonders and Safari') \
        add_circuit_to_map(artistic_circuit, 'purple', 'Artistic and Educational Trip') \
        add_circuit_to_map(adventure_circuit, 'orange', 'Adventure and Exploration') \
        # Add layer control to the map \
        folium.LayerControl().add_to(map_benin) \
        # Save the map to an HTML file \
        map_benin.save('benin_tourist_circuits.html') \
        ''' "
    user_id = "123"                      
    result1 = create_tourist_circuit(message_body, user_id)