import logging
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram import Router
from utils.buttons import get_settings_menu_buttons
from modules.qa.qa_logic import (
    load_config,
    load_tokenizer_and_model,
    generate_response,
)

router = Router()


@router.callback_query(lambda callback: callback.data == "qna")
async def handle_qna_start(callback: types.CallbackQuery, state: FSMContext):
    """
    Обработчик для перехода в режим Q&A.
    """
    await callback.message.answer("Задайте вопрос о боте. Я постараюсь вам помочь!")
    await state.set_state("awaiting_qna_question")


@router.message(StateFilter("awaiting_qna_question"))
async def handle_qna_question(message: types.Message, state: FSMContext):
    """
    Обработчик вопроса пользователя.
    """
    config_path = "/Users/jayanne/Desktop/Projects/BotV2/modules/qa/config.yaml"
    config = load_config(config_path)

    model_name = config.get("model_name", "gpt2")
    tokenizer, model = load_tokenizer_and_model(model_name)

    if not model or not tokenizer:
        await message.answer("Ошибка: не удалось загрузить модель или токенизатор.")
        return

    user_question = message.text
    
    try:
        response, elapsed_time = generate_response(model, tokenizer, user_question, config)
        await message.answer(
            f"Ответ: {response}\n\n(Сгенерировано за {elapsed_time:.2f} сек.)"
        )
        await message.answer("Вы можете настроить параметры или вернуться в главное меню:", reply_markup=get_settings_menu_buttons())
    except Exception as e:
        await message.answer("Произошла ошибка при обработке вашего вопроса. Попробуйте позже.")
        logging.error(f"Ошибка обработки Q&A: {e}")
    finally:
        await state.clear()
        
