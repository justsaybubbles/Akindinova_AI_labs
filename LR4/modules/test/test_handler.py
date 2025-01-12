from aiogram import Router
from aiogram.types import CallbackQuery
from modules.test.test_logic import generate_test_message

router = Router()

@router.callback_query(lambda callback: callback.data == "test")
async def handle_test(callback: CallbackQuery):
    user_id = callback.from_user.id
    message = generate_test_message(user_id)
    
    await callback.message.edit_text(message)
    await callback.answer()  # Закрываем callback
