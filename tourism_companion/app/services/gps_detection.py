import re

# Define keywords and phrases for GPS-based requests
GPS_KEYWORDS = [
    "nearby", "close to me", "around me", "near me", "in my area",
    "restaurants", "hotels", "places to visit", "tourist spots",
    "where can I find", "how to get to", "directions to", "location of"
]

def requires_gps(prompt: str) -> bool:
    """
    Determine if the prompt requires GPS-based information.

    Args:
        prompt (str): The user's prompt.

    Returns:
        bool: True if the prompt requires GPS-based information, False otherwise.
    """
    prompt = prompt.lower()
    for keyword in GPS_KEYWORDS:
        if re.search(r'\b' + re.escape(keyword) + r'\b', prompt):
            return True
    return False
