import time
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import yaml
from typing import Tuple, Union, Optional, Dict


def load_config(file_path: str) -> Dict[str, Union[int, float, str]]:
    """
    Загружает параметры конфигурации из файла .yaml.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_tokenizer_and_model(model_name: str) -> Tuple[Optional[GPT2Tokenizer], Optional[GPT2LMHeadModel]]:
    """
    Загружает токенизатор и модель на основе имени модели.
    """
    try:
        tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        model = GPT2LMHeadModel.from_pretrained(model_name).to("cpu")
        return tokenizer, model
    except Exception as e:
        print(f"Ошибка при загрузке модели {model_name}: {e}")
        return None, None


def generate_response(
    model: GPT2LMHeadModel, tokenizer: GPT2Tokenizer, question: str, config: Dict[str, Union[int, float, str]]
) -> Tuple[str, float]:
    """
    Генерирует текст с помощью модели и заданных параметров, измеряя время выполнения.
    """
    if not model or not tokenizer:
        return "Ошибка: модель или токенизатор отсутствуют.", 0.0

    # Промпт для модели
    prompt = config.get("prompt", "")
    input_text = f"{prompt} {question}"

    try:
        input_ids = tokenizer.encode(input_text, return_tensors="pt")
        start_time = time.time()
        output_ids = model.generate(
            input_ids,
            max_length=config.get("max_length", 50),
            repetition_penalty=config.get("repetition_penalty", 1.2),
            do_sample=True,
            top_k=config.get("top_k", 50),
            top_p=config.get("top_p", 0.95),
            temperature=config.get("temperature", 1.0),
            num_beams=config.get("num_beams", 1),
            no_repeat_ngram_size=config.get("no_repeat_ngram_size", 2),
        )
        elapsed_time = time.time() - start_time
        generated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return generated_text[len(prompt):], elapsed_time
    except Exception as e:
        print(f"Ошибка при генерации текста: {e}")
        return "Ошибка: не удалось сгенерировать текст.", 0.0
