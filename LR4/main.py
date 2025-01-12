import asyncio
import logging
from aiogram                    import Bot, Dispatcher, types
from aiogram.types              import CallbackQuery, FSInputFile
from aiogram.filters            import Command
from aiogram.fsm.context        import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

# импорт своих файлов
from config.config import BOT_TOKEN
from utils.buttons import (
    get_main_menu_buttons,
    get_capabilities_menu_buttons,
    get_learning_modules_buttons,
    get_grammar_menu_buttons,
    get_vocabulary_menu_buttons,
    get_dictionary_menu_buttons,
    get_settings_menu_buttons,
    get_about_menu_buttons,
    get_writing_menu_buttons
)

from modules.dictionary.dictionary_handler  import router as dictionary_router
from modules.grammar.grammar_handler        import router as grammar_router
from modules.writing.writing_handler        import router as writing_router
from modules.test.test_handler              import router as test_router
from modules.qa.qa_handler                  import router as qna_router




from modules.writing.writing_logic          import generate_summary_and_score
from database.activity_handler              import increment_user_activity
from database.activity_view                 import plot_user_activity

import os


# Настройка логирования
logging.basicConfig(level=logging.INFO)


# Создание объектов бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp  = Dispatcher(storage=MemoryStorage())


# Регистрация хэндлеров
dp.include_router(dictionary_router) 
dp.include_router(grammar_router)
dp.include_router(writing_router)
dp.include_router(test_router)
dp.include_router(qna_router)



callback_routes = {
    "main_menu":        lambda: ("Главное меню:",                                       get_main_menu_buttons()),
    "capabilities":     lambda: ("Выберите возможность:",                               get_capabilities_menu_buttons()),
    "learning_modules": lambda: ("Выберите модуль обучения:",                           get_learning_modules_buttons()),
    "grammar":          lambda: ("Грамматика:",                                         get_grammar_menu_buttons()),
    "vocabulary":       lambda: ("Лексика:",                                            get_vocabulary_menu_buttons()),
    "dictionary":       lambda: ("Словарик:",                                           get_dictionary_menu_buttons()),
    "settings":         lambda: ("Настройки:",                                          get_settings_menu_buttons()), 
    "about":            lambda: ("Информация о боте:",                                  get_about_menu_buttons()),
    "writing":          lambda: ("Как хотите ввести текст для проверки?",               get_writing_menu_buttons()),
    "translate_word":   lambda: ("Введите слово на английском для перевода:",           None),
    "grammar_help":     lambda: ("Задайте свой вопрос для консультации по грамматике:", None),
    "submit_text":      lambda: ("Введите текст для анализа:",                          None),
    "submit_image":     lambda: ("Отправьте изображение с текстом:",                    None),
    "confirm":          lambda: ("Текст распознан верно!",                              None),
    "edit":             lambda: ("Надо исправить распознанный текст",                   None),
    "activity":         lambda: ("Статистика использования бота Вами",                  None),
    "test":         lambda: ("Тестовый маршрут активирован.",                  None)
}


# Хэндлер для команды /start
@dp.message(Command("start"))
async def start_command(message: types.Message, state: FSMContext):
    await message.answer(
        "Добро пожаловать! Выберите раздел:",
        reply_markup=get_main_menu_buttons()
    )


@dp.callback_query()
async def menu_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id  # Идентификатор пользователя
    
    # Проверяем, какая callback-данная пришла
    route = callback_routes.get(callback.data)

    if callback.data == "translate_word":
        # Специальная обработка для перевода
        increment_user_activity(user_id, "translate_word")
        await callback.message.edit_text("Введите слово на английском для перевода:")
        await state.set_state("await_word_translation")
        return
    
    if callback.data == "grammar_help":
        # Специальная обработка для консультации по грамматике
        increment_user_activity(user_id, "grammar_help")
        await callback.message.edit_text("Задайте свой вопрос для консультации по грамматике:")
        await state.set_state("await_grammar_question")
        return
    
    if callback.data == "submit_text":
        # Ввод текста
        await callback.message.edit_text("Введите текст для анализа:")
        await state.set_state("await_writing_text")
        return
    
    if callback.data == "submit_image":
        # Ввод изображения
        await callback.message.edit_text("Отправьте изображение для анализа:")
        await state.set_state("await_writing_image")
        return
    
    if callback.data == "confirm":
        # Обработка подтверждения текста
        data = await state.get_data()
        text = data.get("recognized_text", "")
        if text:
            response = await generate_summary_and_score(text)
            await callback.message.edit_text(response, reply_markup=get_writing_menu_buttons())
        else:
            await callback.message.edit_text("Нет текста для анализа. Попробуйте снова.")
        await state.clear()
        return
    
    if callback.data == "edit":
        # Обработка редактирования текста
        data = await state.get_data()
        text = data.get("recognized_text", "")
        if text:
            await callback.message.edit_text(
                f"Распознанный текст:\n{text}\n\nОтредактируйте его и отправьте снова."
            )
            await state.set_state("await_edit")
        else:
            await callback.message.edit_text("Нет текста для редактирования. Попробуйте снова.")
        return
    
    if callback.data == "activity":
        try:
            image_path = plot_user_activity(user_id)

            # Удаляем кнопки из текущего сообщения
            await callback.message.edit_reply_markup()

            # Создаём объект FSInputFile
            photo = FSInputFile(image_path)
            await callback.message.answer_photo(photo, caption="Вот ваша активность!")
            print("График успешно отправлен.")

            # Удаляем временный файл
            os.remove(image_path)

            # Показать меню после отправки графика
            await callback.message.answer(
                "Главное меню:", reply_markup=get_settings_menu_buttons()
            )
        except (FileNotFoundError, ValueError) as e:
            print(f"Обработка ошибки: {e}")
            await callback.message.edit_text(str(e))
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")
            await callback.message.edit_text("Произошла ошибка при построении графика.")
        await callback.answer()
        return

    if callback.data == "qna":
        # Инкремент активности пользователя
        increment_user_activity(callback.from_user.id, "about")
        
        # Отправляем сообщение о запросе вопроса
        await callback.message.edit_text("Введите ваш вопрос, и я постараюсь ответить на него:")
        
        # Устанавливаем состояние для получения вопроса
        await state.set_state("awaiting_qna_question")
        return
        

    if callback.data == "test":
        from modules.test.test_logic import generate_test_message
        message = generate_test_message(user_id)
        await callback.message.edit_text(message)
        await callback.answer()  # Закрываем callback
        return

    if route:
        # Если кнопка соответствует маршруту из callback_routes
        message_text, buttons = route()

        # Инкрементируем активность в зависимости от маршрута
        activity_mapping = {
            "grammar_tenses": "grammar_tenses", 
            "grammar_structures": "grammar_structures", 
            "modal_verbs": "modal_verbs", 
            "grammar_help": "grammar_help", 
            "new_words": "new_words", 
            "word_formation": "word_formation",
            "writing": "writing", 
            "translate_word": "translate_word", 
            "word_book": "word_book", 
            "level_check": "level_check", 
            "about": "about"
        }
        
        # Если callback соответствует секции, записываем активность
        section = activity_mapping.get(callback.data)
        if section:
            increment_user_activity(user_id, section)
        
        await callback.message.edit_text(message_text, reply_markup=buttons)
    else:
        # Обработка неизвестных callback-данных
        await callback.answer("Неподдерживаемая команда", show_alert=True)
    
    await callback.answer()  # Закрываем callback



# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
