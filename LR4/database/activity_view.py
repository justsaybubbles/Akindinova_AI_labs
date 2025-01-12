import json
import os
import matplotlib.pyplot as plt

def get_user_activity(user_id):
    """
    Возвращает данные активности пользователя в виде строки.
    
    Args:
        user_id (int): Идентификатор пользователя.

    Returns:
        str: Данные активности пользователя в формате JSON.
    """
    file_path = "/Users/jayanne/Desktop/Projects/BotV2/database/activity_logs.json"  # Путь к JSON файлу

    # Проверяем существование файла
    if not os.path.exists(file_path):
        raise FileNotFoundError("Файл activity_logs.json не найден.")

    # Загружаем данные
    with open(file_path, "r") as file:
        data = json.load(file)

    # Получаем данные для указанного пользователя
    user_data = data.get(str(user_id))
    if not user_data:
        raise ValueError("Нет данных для данного пользователя.")

    # Форматируем данные в виде строки
    user_activity_str = json.dumps({str(user_id): user_data}, indent=4, ensure_ascii=False)
    return user_activity_str

def plot_user_activity(user_id):
    file_path = "/Users/jayanne/Desktop/Projects/BotV2/database/activity_logs.json"

    # Проверяем существование файла активности
    if not os.path.exists(file_path):
        raise FileNotFoundError("Файл activity_logs.json не найден.")

    # Загружаем данные
    with open(file_path, "r") as file:
        data = json.load(file)

    # Проверяем, есть ли данные для указанного пользователя
    user_data = data.get(str(user_id))
    print(user_data)
    if not user_data:
        raise ValueError("Нет данных для данного пользователя.")

    # Построение гистограммы
    activity_keys = user_data.keys()
    activity_values = user_data.values()

    plt.figure(figsize=(10, 6))
    plt.bar(activity_keys, activity_values, color="skyblue")
    plt.xlabel("Разделы")
    plt.ylabel("Количество переходов")
    plt.title("Активность пользователя")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    output_path = f"/Users/jayanne/Desktop/Projects/BotV2/database/user_{user_id}_activity.png"
    plt.savefig(output_path)
    
    return output_path