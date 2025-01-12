import os
import httpx
from typing import Optional
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")

async def get_grammar_answer(question: str) -> Optional[str]:
    """
    Отправляет запрос к Llama 3 через Rapid API для получения ответа на вопрос по грамматике.
    """
    url = "https://llama-3.p.rapidapi.com/llama3"
    payload = {
        "prompt": question,
        "system_prompt":
            "You are a formal grammar consultant. Provide detailed and accurate answers to questions about English grammar. Do not repeat the question. Avoid casual language, emojis, greetings and farewells."
    }
    headers = {
        "x-rapidapi-key": LLAMA_API_KEY,
        "x-rapidapi-host": "llama-3.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json().get("msg", "No response provided.")
            else:
                return f"Error: API responded with status code {response.status_code}"
    except httpx.RequestError as e:
        print(response)
        return f"Request error: {str(e)}"
        