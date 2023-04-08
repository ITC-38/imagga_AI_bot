from aiogram.types import KeyboardButton

from commands import Commands


GET_PHOTO_OBJ = KeyboardButton(Commands.get_obj.value)
BARCODE_SCAN_BUTTON = KeyboardButton(Commands.barcodes.value)
