import json

FILE_PATH = "/Users/jayanne/Desktop/Projects/BotV2/database/activity_logs.json"

def load_activity_logs():
    """Загружает логи активности из файла."""
    try:
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_activity_logs(data):
    """Сохраняет логи активности в файл."""
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)

def increment_user_activity(user_id, section):
    """Обновляет активность пользователя в указанном разделе."""
    data = load_activity_logs()
    user_id = str(user_id)

    # Если пользователь не существует, инициализируем его данные
    if user_id not in data:
        data[user_id] = {key: 0 for key in [
            "grammar_tenses", "grammar_structures", "modal_verbs", "grammar_help", 
            "new_words", "word_formation",
            "writing", 
            "translate_word", "word_book", 
            "level_check", 
            "about"
        ]}
    
    # Увеличиваем счетчик для указанного раздела
    if section in data[user_id]:
        data[user_id][section] += 1
    else:
        raise ValueError(f"Раздел {section} не существует.")

    # Сохраняем обновления
    save_activity_logs(data)

def get_user_activity(user_id):
    """Возвращает статистику активности пользователя."""
    data = load_activity_logs()
    return data.get(str(user_id), None)
