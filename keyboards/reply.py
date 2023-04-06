from aiogram.types import ReplyKeyboardMarkup

from buttons.reply import GET_PHOTO_OBJ

START_COMMANDS_KEYBOARD = ReplyKeyboardMarkup([
    [GET_PHOTO_OBJ],
], resize_keyboard=True)
