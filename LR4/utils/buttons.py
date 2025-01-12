from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Главное меню
def get_main_menu_buttons():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Возможности",               callback_data="capabilities")],
        [InlineKeyboardButton(text="Настройки",                 callback_data="settings")],
        [InlineKeyboardButton(text="О боте",                    callback_data="about")]
    ])


# Меню "Возможности"
def get_capabilities_menu_buttons():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Модули обучения",           callback_data="learning_modules")],
        [InlineKeyboardButton(text="Словарик",                  callback_data="dictionary")],
        [InlineKeyboardButton(text="Назад",                     callback_data="main_menu")]
    ])


# Меню "Модули обучения"
def get_learning_modules_buttons():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Грамматика",                callback_data="grammar")],
        [InlineKeyboardButton(text="Лексика",                   callback_data="vocabulary")],
        [InlineKeyboardButton(text="Письменные задания",        callback_data="writing")],
        [InlineKeyboardButton(text="Назад",                     callback_data="capabilities")]
    ])


# Меню "Грамматика"
def get_grammar_menu_buttons():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Правила по временам",        callback_data="grammar_tenses")],
        [InlineKeyboardButton(text="Грамматические обороты",     callback_data="grammar_turns")],
        [InlineKeyboardButton(text="Модальные глаголы",          callback_data="modal_verbs")],
        [InlineKeyboardButton(text="Консультация по грамматике", callback_data="grammar_help")],
        [InlineKeyboardButton(text="Назад",                      callback_data="learning_modules")]
    ])


# Меню "Лексика"
def get_vocabulary_menu_buttons():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Новые слова",               callback_data="new_words")],
        [InlineKeyboardButton(text="Словообразование",          callback_data="word_formation")],
        [InlineKeyboardButton(text="Назад",                     callback_data="learning_modules")]
    ])


# Меню "Словарик"
def get_dictionary_menu_buttons():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Перевод слов",              callback_data="translate_word")],
        [InlineKeyboardButton(text="Сохраненные слова",         callback_data="save_translation")],
        [InlineKeyboardButton(text="Назад",                     callback_data="capabilities")]
    ])


def get_writing_menu_buttons():
    buttons = [
        [InlineKeyboardButton(text="По сообщению",              callback_data="submit_text")],
        [InlineKeyboardButton(text="По изображению",            callback_data="submit_image")],
        [InlineKeyboardButton(text="Назад",                     callback_data="learning_modules")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_edit_buttons():
    buttons = [
        [InlineKeyboardButton(text="Все верно",                 callback_data="confirm")],
        [InlineKeyboardButton(text="Изменить",                  callback_data="edit")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Меню "Настройки"
def get_settings_menu_buttons():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Выбор уровня",              callback_data="choose_level")],
        [InlineKeyboardButton(text="Тест",                      callback_data="test")],
        [InlineKeyboardButton(text="Активность",                callback_data="activity")],
        [InlineKeyboardButton(text="Назад",                     callback_data="main_menu")]
    ])


# Меню "О боте"
def get_about_menu_buttons():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Q&A",                       callback_data="qna")],
        [InlineKeyboardButton(text="Назад",                     callback_data="main_menu")]
    ])


# Общая функция для добавления кнопки "Назад"
def add_back_button(buttons, callback_data):
    buttons.inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data=callback_data)])
    return buttons
