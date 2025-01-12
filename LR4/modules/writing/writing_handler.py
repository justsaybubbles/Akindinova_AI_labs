from aiogram                        import Router
from aiogram.filters                import StateFilter
from aiogram.types                  import Message, CallbackQuery
from aiogram.client.session         import aiohttp
from aiogram.fsm.context            import FSMContext
from io                             import BytesIO
from PIL                            import Image
from modules.writing.writing_logic  import extract_text, generate_summary_and_score, cv2, np
from utils.buttons                  import get_writing_menu_buttons, get_edit_buttons

router = Router()

# Обработка текста
@router.message(StateFilter("await_writing_text"))
async def process_text_submission(message: Message, state: FSMContext):
    text = message.text.strip()
    response = await generate_summary_and_score(text)
    await message.answer(response, reply_markup=get_writing_menu_buttons())
    await state.clear()


# Обработка изображения
@router.message(StateFilter("await_writing_image"))
@router.callback_query(StateFilter("await_writing_image"))
async def process_image_submission(event: Message | CallbackQuery, state: FSMContext):
    if isinstance(event, Message):
        # Обработка сообщения
        if not event.photo:
            await event.answer("Пожалуйста, отправьте изображение.")
            return

        # Получаем объект фотографии (самое большое доступное разрешение)
        photo = event.photo[-1]
        file = await event.bot.get_file(photo.file_id)
        file_path = file.file_path

        # Загружаем содержимое файла
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.telegram.org/file/bot{event.bot.token}/{file_path}") as response:
                if response.status != 200:
                    await event.answer("Ошибка при загрузке изображения. Попробуйте еще раз.")
                    return

                file_bytes = await response.read()
                image = Image.open(BytesIO(file_bytes))

                # Конвертируем PIL.Image в формат OpenCV
                image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                
                # Распознаем текст
                text = extract_text(image_cv)

                # Сохраняем текст в состояние и отправляем пользователю
                await state.update_data(recognized_text=text)
                await event.answer(
                    f"Распознанный текст:\n{text}\n\nВсе верно?", 
                    reply_markup=get_edit_buttons()
                )


@router.message(StateFilter("await_edit"))
async def process_corrected_text(message: Message, state: FSMContext):
    text = message.text.strip()
    response = await generate_summary_and_score(text)
    await message.answer(response, reply_markup=get_writing_menu_buttons())
    await state.clear()
