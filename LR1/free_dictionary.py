import requests

def fetch_free_dict_definition(word, lang) -> str:
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/{lang}/{word}"
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()
        if isinstance(result, list) and result:
            return result[0]['meanings'][0]['definitions'][0]['definition']
        return 'No definition found.'
    except Exception as e:
        return f"Error: {e}"
