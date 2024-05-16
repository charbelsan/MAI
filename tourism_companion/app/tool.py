from langchain.tools import Tool
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.summarize import load_summarize_chain
from app.services.google_search import google_search
from app.config import Config
# from langchain.utilities import GoogleSearchAPIWrapper
# from langchain.utilities import WolframAlphaAPIWrapper, OpenWeatherMapAPIWrapper
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain_community.utilities import WolframAlphaAPIWrapper
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.utilities import GoogleSearchAPIWrapper



from langchain_community.llms import OpenAI
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = OpenAI(model_name="gpt-4o", api_key=OPENAI_API_KEY)

# google_api_key = Config.GOOGLE_API_KEY
# google_cse_id = Config.GOOGLE_CSE_ID

# class GoogleSearchTool(Tool):
#     name = "google_search"
#     description = "Perform a Google search using the Custom Search API."

#     def run(self, query: str):
#         return google_search(query, google_api_key, google_cse_id)

# # Define the tool for Google search
# google_search_tool = GoogleSearchTool()

# Define the tools
search = GoogleSearchAPIWrapper(k=2)
wikipedia = WikipediaAPIWrapper()
wolfram_alpha = WolframAlphaAPIWrapper()
weather = OpenWeatherMapAPIWrapper()

search_tool = Tool(
            name="Search by Google",
            func=search.run,
            description="Useful when you need to answer questions about current events and real-time information in Benin."
            "Providing information about tourist attractions, landmarks, and cultural sites in Benin."
            "Giving travel advice, including transportation, accommodation, and dining options in Benin."
            "Offering general tips on local customs, weather, and safety in Benin."
            "Performing web searches to provide relevant information based on user queries in Benin."
            "Determining if the request needs GPS information to find nearby places like restaurants, hotels, or tourist spots in Benin."
        )

Wolfram_tool =  Tool(
                name='Wolfram Alpha',
                func=wolfram_alpha.run,
                description="Useful for when you need to answer questions about Math, "
                            "Science, Technology, Culture, people, Society and Everyday Life."
                            "Input should be a search query"
            )

Weather_tool = Tool(
            name='Weather',
            func=weather.run,
            description="Useful for when you need to answer questions about weather in Benin."
            "Offering general tips on local weather in Benin."
        )


wikisummarize = load_summarize_chain(llm, chain_type="stuff")
class WikiPage:
    def __init__(self, title, summary):
        self.title = title
        self.page_content = summary
        self.metadata = {}

def wiki_summary(search_query: str) -> str:
    wikipedia_wrapper = wikipedia
    wiki_result = wikipedia_wrapper.run(search_query)
    # print(wiki_result)

    if not wiki_result:
        return "No good Wikipedia Search Result was found"

    wiki_pages = []
    for section in wiki_result.split("\n\n"):
        title, summary = section.split("\nSummary: ", 1)
        title = title.replace("Page: ", "") 
        wiki_pages.append(WikiPage(title=title, summary=summary))

    summary_result = wikisummarize.run(wiki_pages)
    return summary_result

wiki_tool = Tool(
            name="Wikipedia",
            func=wiki_summary,
            description="Useful for searching information on historical information on Wikipedia about Benin."
            "Providing information about tourist attractions, landmarks, and cultural sites in Benin."
            "Giving travel advice, including transportation, accommodation, and dining options in Benin."
            "Offering general tips on local customs, weather, and safety in Benin."
            "Performing web searches to provide relevant information based on user queries in Benin."
            "Find nearby places like restaurants, hotels, or tourist spots in Benin."
        )