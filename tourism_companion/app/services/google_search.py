# import requests

# def google_search(query, api_key, cse_id):
#     """
#     Perform a Google search using the Custom Search API.

#     Args:
#         query (str): The search query.
#         api_key (str): The API key for the Google Custom Search API.
#         cse_id (str): The Custom Search Engine ID.

#     Returns:
#         list: A list of search results.
#     """
#     url = f"https://www.googleapis.com/customsearch/v1"
#     params = {
#         "q": query,
#         "key": api_key,
#         "cx": cse_id
#     }
#     response = requests.get(url, params=params)
#     results = response.json().get('items', [])
#     return results
import requests

def google_search(query, api_key, cx):
    """
    Perform a Google search using the specified query, API key, and search engine ID (cx).

    Args:
        query (str): The search query.
        api_key (str): The Google API key.
        cx (str): The custom search engine ID.

    Returns:
        list: A list of search results.
    """
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}"
    response = requests.get(url)
    response.raise_for_status()
    results = response.json().get('items', [])
    return results
