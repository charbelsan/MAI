from langchain.tools import Tool
from googleapiclient.discovery import build
from app.config import Config

class GoogleSearchTool(Tool):
    def __init__(self):
        self.service = build("customsearch", "v1", developerKey=Config.GOOGLE_API_KEY)
        self.cse_id = Config.GOOGLE_CSE_ID
        super().__init__(
            name="Google Search",
            func=self.search,
            description="Searches Google for relevant information."
        )

    def search(self, query):
        res = self.service.cse().list(q=query, cx=self.cse_id).execute()
        return res.get('items', [])



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
