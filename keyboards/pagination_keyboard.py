from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.lexicon import LEXICON_RU

def create_pagination_keyboard(page: int = 1, pages: int = 10) -> InlineKeyboardMarkup:
    pag_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=LEXICON_RU['PREV_BUTTON'] if page > 1 else '✖️', callback_data='previous_button' if page > 1 else 'error_alert'),
                InlineKeyboardButton(text=f'{page} из {pages}', callback_data='add_to_favourite'),
                InlineKeyboardButton(text=LEXICON_RU['NEXT_BUTTON'] if page < 250 else '✖️', callback_data='next_button' if page < 250 else 'error_alert')
            ],
            [
                InlineKeyboardButton(text=LEXICON_RU['CANCEL_BUTTON'], callback_data='cancel_button')
            ]
        ], 
        resize_keyboard=True
    )

    return pag_kb