from aiogram                        import Router
from aiogram.filters                import StateFilter
from aiogram.fsm.context            import FSMContext
from aiogram.types                  import Message
from modules.grammar.grammar_logic  import get_grammar_answer
from utils.buttons                  import get_grammar_menu_buttons


router = Router()

# Обработчик для вопросов по грамматике
@router.message(StateFilter("await_grammar_question"))
async def handle_grammar_question(message: Message, state: FSMContext):
    user_question = message.text.strip()

    if not user_question:
        await message.answer("Введите корректный вопрос по грамматике.")
        return

    await message.answer("Пожалуйста, подождите, пока я найду ответ...")

    # Получение ответа от Llama 3
    answer = await get_grammar_answer(user_question)
    await message.answer(f"Ответ:\n{answer}")

    # Возврат в меню грамматики
    await message.answer(
        "Вернуться в меню грамматики:",
        reply_markup=get_grammar_menu_buttons()
    )
    await state.clear()
