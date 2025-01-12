from modules.dictionary.dictionary_logic import Translator
from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from utils.buttons import get_dictionary_menu_buttons

translator = Translator()
router = Router()

# Обработчик для обработки слова
@router.message(StateFilter("await_word_translation"))
async def process_word_translation(message: Message, state: FSMContext):
    word = message.text.strip()  # Получаем слово от пользователя
    
    if not word.isalpha():
        await message.answer("Введите корректное слово на английском.")
        return
    
    # Обработка слова через асинхронный Translator
    result = await translator.process_word(word)  # Асинхронный вызов
    await message.answer(f"Результат перевода:\n{result}")
    
    # Возвращаем пользователя в меню словарика
    await message.answer(
        "Вернуться в словарик:",
        reply_markup=get_dictionary_menu_buttons()
    )
    await state.clear()
