from langchain.tools import Tool
from app.services.google_search import google_search
from app.config import Config

google_api_key = Config.GOOGLE_API_KEY
google_cse_id = Config.GOOGLE_CSE_ID

class GoogleSearchTool(Tool):
    name = "google_search"
    description = "Perform a Google search using the Custom Search API."

    def run(self, query: str):
        return google_search(query, google_api_key, google_cse_id)

# Define the tool for Google search
google_search_tool = GoogleSearchTool()



# from langchain.tools import Tool
# from app.services.places_search import search_nearby_places
# from app.config import Config

# google_api_key = Config.GOOGLE_API_KEY

# class SearchPlacesTool(Tool):
#     name = "search_places"
#     description = "Search for nearby places based on GPS position and place type."

#     def run(self, gps_position: str, place_type: str):
#         return search_nearby_places(gps_position, place_type, google_api_key)

# # Define specific tools for different place types
# search_restaurants_tool = SearchPlacesTool(name="search_restaurants", description="Search for nearby restaurants.")
# search_hotels_tool = SearchPlacesTool(name="search_hotels", description="Search for nearby hotels.")
# search_tourist_spots_tool = SearchPlacesTool(name="search_tourist_spots", description="Search for nearby tourist spots.")
