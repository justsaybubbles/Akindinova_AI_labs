import requests
from env_loader import get_env_var

def fetch_merriam_definition(word) -> str:
    try:
        api_key = get_env_var("MERRIAM_API_KEY")
        url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()
        if isinstance(result, list) and 'shortdef' in result[0]:
            return result[0]['shortdef'][0]
        return 'No definition found.'
    except Exception as e:
        return f"Error: {e}"
