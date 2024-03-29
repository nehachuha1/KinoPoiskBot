from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.filters.callback_data import CallbackData

from lexicon.lexicon import LEXICON_RU
from keyboards.main_menu import main_menu_keyboard, cancel_keyboard
from keyboards.favourite_keyboard import make_favourite_kb
from keyboards.pagination_keyboard import create_pagination_keyboard
from filters.film_name import FilmNameCallbackFactory
from config.config import db, cached_db

import logging

router = Router()

logger = logging.getLogger(__name__)
logging.basicConfig(
         level=logging.INFO, format='%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s')
logger.info('User Handler Logger activated...')

@router.message(CommandStart())
async def process_start_command(message: Message):
    db.registration_row(message.from_user.id, message.from_user.full_name)
    cached_db.set_values(str(message.from_user.id), db.get_user_info(str(message.from_user.id)))
    await message.answer(
        text=f"<b>{LEXICON_RU['START_DESC']}</b>",
        parse_mode='HTML',
        reply_markup=main_menu_keyboard
    )

@router.callback_query(F.data.in_(['cancel_button']))
async def process_cancel_button(callback: CallbackQuery):
    await callback.message.edit_text(
        text=f"<b>{LEXICON_RU['START_DESC']}</b>",
        reply_markup=main_menu_keyboard
    )

@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        text=LEXICON_RU['INFO_DESC'],
        reply_markup=cancel_keyboard
    )

@router.message(Command(commands=['stats']))
async def process_help_command(message: Message):
    await message.edit_text(
        text='В разработке...',
        reply_markup=cancel_keyboard,   
    )

@router.callback_query(F.data.in_(['info_desc_show']))
async def process_info_show_button(callback: CallbackQuery):
    await callback.message.edit_text(
        text=f"<b>{LEXICON_RU['INFO_DESC']}</b>",
        parse_mode='HTML',
        reply_markup=cancel_keyboard
    )

@router.callback_query(F.data.in_(['favourite_show']))
async def process_favourite_show_button(callback: CallbackQuery):
    # kb = make_favourite_kb(username=callback.from_user.id)
    # await callback.message.edit_text(
    #     parse_mode='HTML',
    #     text=LEXICON_RU['FAVOURITE_MESSAGE'],
    #     reply_markup=kb
    # )
    await callback.message.edit_text(
        parse_mode='HTML',
        text='<b>В разработке...</b>',
        reply_markup=cancel_keyboard)

@router.callback_query(F.data.in_(['check_top_show']))
async def process_check_top(callback: CallbackQuery):
    current_user_data = cached_db.get_values(str(callback.from_user.id))
    current_film = db.get_film([int(x) for x in current_user_data[0]][0])

    current_keyboard = create_pagination_keyboard([int(x) for x in current_user_data[0]][0], 250)

    film_data, position = *current_film[0], current_film[1]
    await callback.message.edit_text(
        parse_mode='HTML',
        text=LEXICON_RU['FILM_INFO_DESC'].format(
            film_place=film_data[5], 
            film_name=film_data[4],
            film_rating=film_data[1],
            film_year=film_data[2],
            film_country=film_data[0],
            film_url=film_data[3]
            ),
            reply_markup=current_keyboard
    )

@router.callback_query(F.data.in_(['previous_button']))
async def process_left_button(callback: CallbackQuery):
    current_user_data = cached_db.get_values(str(callback.from_user.id))
    cached_db.set_values(str(callback.from_user.id), [([int(x) - 1 for x in current_user_data[0]])])
    current_user_data = cached_db.get_values(str(callback.from_user.id))
    current_film = db.get_film([int(x) for x in current_user_data[0]][0])

    current_keyboard = create_pagination_keyboard([int(x) for x in current_user_data[0]][0], 250)

    film_data, position = *current_film[0], current_film[1]
    await callback.message.edit_text(
        parse_mode='HTML',
        text=LEXICON_RU['FILM_INFO_DESC'].format(
            film_place=film_data[5], 
            film_name=film_data[4],
            film_rating=film_data[1],
            film_year=film_data[2],
            film_country=film_data[0],
            film_url=film_data[3]
            ),
            reply_markup=current_keyboard
    )

@router.callback_query(F.data.in_(['next_button']))
async def process_right_button(callback: CallbackQuery):
    current_user_data = cached_db.get_values(str(callback.from_user.id))
    cached_db.set_values(str(callback.from_user.id), [([int(x) + 1 for x in current_user_data[0]])])
    current_user_data = cached_db.get_values(str(callback.from_user.id))
    current_film = db.get_film([int(x) for x in current_user_data[0]][0])

    current_keyboard = create_pagination_keyboard([int(x) for x in current_user_data[0]][0], 250)

    film_data, position = *current_film[0], current_film[1]
    await callback.message.edit_text(
        parse_mode='HTML',
        text=LEXICON_RU['FILM_INFO_DESC'].format(
            film_place=film_data[5], 
            film_name=film_data[4],
            film_rating=film_data[1],
            film_year=film_data[2],
            film_country=film_data[0],
            film_url=film_data[3]
            ),
            reply_markup=current_keyboard
    )

@router.callback_query(F.data.in_(['add_to_favourite']))
async def process_add_to_favourite(callback: CallbackQuery):
    # current_user_data = cached_db.get_values(str(callback.from_user.id))
    # current_film = db.get_film([int(x) for x in current_user_data[0]][0])

    # film_data, position = *current_film[0], current_film[1]
    # db.add_to_favourite(film=film_data[4], username=callback.from_user.id)
    # await callback.answer(text='Фильм успешно добавлен в избранное!')
    await callback.answer('')

# @router.callback_query(FilmNameCallbackFactory.filter())
# async def process_get_link_to_film_from_favourite(callback: CallbackQuery, callback_data: CallbackData):
#     current_film = callback_data.film_name
#     link_for_film = db.get_link_from_favourite(film_name=current_film)

#     await callback.message.answer(
#         parse_mode='HTML',
#         text=f'<b>Ссылка на фильм "{current_film}":\n\n{link_for_film}</b>'
#     )

@router.callback_query(F.data.in_(['error_alert']))
async def process_show_alert(callback: CallbackQuery):
    await callback.answer(
        parse_mode='HTML',
        text='❗️ Ошибка',
        show_alert=True
        )

@router.callback_query()
async def process_any_callback(callback: CallbackQuery):
    await callback.answer(callback.data)