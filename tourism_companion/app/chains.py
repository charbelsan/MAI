from langchain.chains import SimpleChain
from app.agent import tourism_agent

class SearchChain(SimpleChain):
    def __init__(self, input):
        super().__init__(input=input, agent=tourism_agent)

    def run(self):
        gps_position = self.input.get("gps_position")
        place_type = self.input.get("place_type")
        if not gps_position or not place_type:
            return "Please provide both GPS position and place type."

        # Run the agent with the input
        return self.agent.run(gps_position=gps_position, place_type=place_type)

# Example chain usage
def search_nearby(gps_position, place_type):
    chain = SearchChain(input={"gps_position": gps_position, "place_type": place_type})
    return chain.run()
