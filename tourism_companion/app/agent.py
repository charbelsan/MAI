from langchain.agents import Agent
from app.tools import google_search_tool

class TourismAgent(Agent):
    tools = [google_search_tool]

    def __init__(self, model):
        super().__init__(tools=self.tools, model=model)
        self.name = "TourismAgent"
        self.description = "A tourism companion agent that can provide information based on user queries."

# Initialize the TourismAgent with GPT-4
from langchain.llms import OpenAI
gpt4_model = OpenAI(model_name="text-davinci-003")
tourism_agent = TourismAgent(model=gpt4_model)
