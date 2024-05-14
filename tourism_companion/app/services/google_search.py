import requests

def google_search(query, api_key, cse_id):
    """
    Perform a Google search using the Custom Search API.

    Args:
        query (str): The search query.
        api_key (str): The API key for the Google Custom Search API.
        cse_id (str): The Custom Search Engine ID.

    Returns:
        list: A list of search results.
    """
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": cse_id
    }
    response = requests.get(url, params=params)
    results = response.json().get('items', [])
    return results
