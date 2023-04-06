import datetime
import os

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType, ReplyKeyboardRemove

from commands import Commands
from config import load_config, BASE_DIR, IMAGGA_PHOTOS_DIR
from keyboards.reply import START_COMMANDS_KEYBOARD
from states import GetPhotoObjectState

BOT_CONFIG = load_config(BASE_DIR / '.env')
storage = MemoryStorage()
bot = Bot(BOT_CONFIG['bot_token'])
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'], commands_prefix='/!')
async def start(message: Message):
    await message.reply(
        'Привет! Я Imagga бот!',
        reply_markup=START_COMMANDS_KEYBOARD
    )


if __name__ == '__main__':
    if not os.path.exists(IMAGGA_PHOTOS_DIR):
        os.makedirs(IMAGGA_PHOTOS_DIR)
    executor.start_polling(dp)
