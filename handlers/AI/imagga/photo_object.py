import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, ContentType, InputFile

from api_clients.imagga.tags import ImaggaTagsEndpoint
from commands import Commands
from config import IMAGGA_PHOTOS_DIR
from keyboards.reply import START_COMMANDS_KEYBOARD
from loader import dp
from misc.states import GetPhotoObjectState


@dp.message_handler(text=Commands.get_obj.value)
async def get_photo_object_command(message: Message):
    await GetPhotoObjectState.send_photo.set()
    await message.answer(
        'Отправьте мне картинку либо ссылку на неё',
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message_handler(content_types=[ContentType.PHOTO], state=GetPhotoObjectState.send_photo)
async def get_photo_object(message: Message, state: FSMContext):
    file = await message.photo[0].get_file()
    file_format = file.values['file_path'].split('.')[-1]
    date_name = datetime.datetime.now()
    file_obj = await message.bot.download_file_by_id(
        file.file_id,
        f'{IMAGGA_PHOTOS_DIR}/{date_name.date()}/'
        f'photo_{date_name.time().__str__().replace(":", "-")}.{file_format}'
    )
    loader = ImaggaTagsEndpoint(
        message.bot['config']['imagga_api_key'],
        message.bot['config']['imagga_api_secret']
    )
    await message.answer(
        'Фото обрабатывается...',
        reply_markup=START_COMMANDS_KEYBOARD
    )
    with open(file_obj.name, 'rb') as file:
        content = file.read()
    response = loader.send_photo_bytes(content)
    if isinstance(response, (int, str)):
        await message.answer(f'Что-то пошло не так... Код ошибки: {response}')
    else:
        object_dict = response["result"]["tags"][0]
        await message.bot.send_photo(
            message.from_user.id,
            InputFile(file_obj.name),
            caption=f'Успешно обработал!\n'
                    f'Объект на картинке похож на '
                    f'{object_dict["tag"][loader.lang]}\n'
                    f'Процент совпадение: {object_dict["confidence"]}%'
        )
    await state.finish()


@dp.message_handler(content_types=[ContentType.TEXT], state=GetPhotoObjectState.send_photo)
async def get_photo_object(message: Message, state: FSMContext):
    if not message.text.startswith(('http:', 'https:')) or message.text.split('.')[-1].lower() not in ['jpg', 'png', 'jpeg']:
        await message.answer('Дурак-простак, введи прямую ссылку на файл')
        return
    loader = ImaggaTagsEndpoint(
        message.bot['config']['imagga_api_key'],
        message.bot['config']['imagga_api_secret']
    )
    await message.answer(
        'Фото обрабатывается...',
        reply_markup=START_COMMANDS_KEYBOARD
    )
    response = loader.send_photo_bytes(message.text)
    if isinstance(response, (int, str)):
        await message.answer(f'Что-то пошло не так... Код ошибки: {response}')
    else:
        object_dict = response["result"]["tags"][0]
        await message.answer(
            f'Успешно обработал!\n'
            f'Объект на картинке похож на '
            f'{object_dict["tag"][loader.lang]}\n'
            f'Процент совпадение: {object_dict["confidence"]}%'
        )
    await state.finish()
