from lexicon.lexicon import LEXICON_RU
from config.config import db

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from filters.film_name import FilmNameCallbackFactory

def make_favourite_kb(username: str) -> InlineKeyboardBuilder:
    
    favourite_films = db.get_favourite(username=username)
    kb = InlineKeyboardBuilder()

    for film_name in favourite_films:
        kb.add(InlineKeyboardButton(text=film_name, callback_data=FilmNameCallbackFactory(film_name=film_name).pack()))
    
    kb.add(InlineKeyboardButton(text=LEXICON_RU['CANCEL_BUTTON'], callback_data='cancel_button'))
    
    kb.adjust(1)
    return kb.as_markup()