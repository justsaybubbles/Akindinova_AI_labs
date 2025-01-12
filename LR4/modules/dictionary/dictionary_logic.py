import os
import json
from typing import Optional, Dict, List
from dotenv import load_dotenv
import httpx
from aiofile import async_open

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение API-ключей из переменных окружения
API_KEY_RAPID: str = os.getenv("RAPID_TRANSLATE_API_KEY", "")
MERRIAM_API_KEY = os.getenv("MERRIAM_API_KEY")
NINJA_API_KEY = os.getenv("NINJA_API_KEY")

# Асинхронная функция для перевода текста через Rapid Translate API
async def get_translation_from_rapid(word: str, source_lang: str, target_lang: str) -> Optional[str]:
    url: str = "https://rapid-translate-multi-traduction.p.rapidapi.com/t"
    headers: Dict[str, str] = {
        "x-rapidapi-key": API_KEY_RAPID,
        "x-rapidapi-host": "rapid-translate-multi-traduction.p.rapidapi.com",
    }
    payload: Dict[str, str] = {"q": word, "from": source_lang, "to": target_lang}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()[0]
    return None

# Асинхронная функция для получения синонимов через Ninja Thesaurus API
async def get_synonyms(word: str) -> List[str]:
    api_url = f"https://api.api-ninjas.com/v1/thesaurus?word={word}"
    headers = {"X-Api-Key": NINJA_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, headers=headers)

    if response.status_code == httpx.codes.OK:
        data = response.json()
        return data.get("synonyms", [])[:3]
    return []

# Асинхронная функция для получения определения через Merriam-Webster API
async def get_definition(word: str) -> str:
    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={MERRIAM_API_KEY}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and len(result) > 0 and "shortdef" in result[0]:
            return result[0]["shortdef"][0]
        return "No definition found."
    return f"Error: Merriam-Webster API responded with {response.status_code}"

# Асинхронная функция для сохранения переведенного слова в файл
async def save_translation_to_file(english_word: str, translated_word: str, file_path: str = "saved_words.json") -> None:
    data = {}

    # Чтение текущих данных из файла
    try:
        async with async_open(file_path, mode="r", encoding="utf-8") as file:
            content = await file.read()
            data = json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    # Добавление нового перевода
    data[english_word] = translated_word

    # Запись обновленных данных в файл
    async with async_open(file_path, mode="w", encoding="utf-8") as file:
        await file.write(json.dumps(data, ensure_ascii=False, indent=4))

# Класс для перевода и получения данных
class Translator:
    async def process_word(self, text: str) -> str:
        # Переводим слово с английского на русский
        translated_word = await get_translation_from_rapid(text, "en", "ru")

        if translated_word is None:
            return "Ошибка при переводе."

        # Получаем синонимы и определение
        synonyms = await get_synonyms(text)
        definition = await get_definition(text)

        # Формируем результат
        result = f"{translated_word}\n{text} (en)\n"
        result += f"синонимы: {', '.join(synonyms)}\n" if synonyms else "синонимы: не найдены\n"
        result += f"определение: {definition}"

        return result
