from keyboards.pagination_keyboard import create_pagination_keyboard
from lexicon.lexicon import LEXICON_RU

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

favourite_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=LEXICON_RU['CANCEL_BUTTON'], callback_data='cancel_button')
        ],
    ], resize_keyboard=True)