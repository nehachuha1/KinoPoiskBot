from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.lexicon import LEXICON_RU

main_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=LEXICON_RU['INFO_BUTTON'], callback_data='info_desc_show'),
            InlineKeyboardButton(text=LEXICON_RU['FAVOURITE_BUTTON'], callback_data='favourite_show')
        ],
        [
            InlineKeyboardButton(text=LEXICON_RU['CHECK_TOP_BUTTON'], callback_data='check_top_show')
        ]
    ],
    resize_keyboard=True
)

cancel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=LEXICON_RU['CANCEL_BUTTON'], callback_data='cancel_button')
        ]
    ],
    resize_keyboard=True
)
