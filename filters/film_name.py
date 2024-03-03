from aiogram.filters.callback_data import CallbackData

class FilmNameCallbackFactory(CallbackData, prefix='film_name'):
    film_name: str