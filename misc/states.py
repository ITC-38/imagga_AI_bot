from aiogram.dispatcher.filters.state import StatesGroup, State


class GetPhotoObjectState(StatesGroup):
    send_photo = State()
