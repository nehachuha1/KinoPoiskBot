import asyncio
import logging

from aiogram import Bot, Dispatcher

from handlers import other_handler, user_handler
# from keyboards.main_menu import set_main_menu
from config.config import Config, load_config, db, cached_db

logger = logging.getLogger(__name__)

async def main() -> None:
    
    logging.basicConfig(
         level=logging.INFO, format='%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot...')

    # db.add_top_250_films()
    config: Config = load_config('.env')
    
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher()

    dp.include_router(user_handler.router)
    dp.include_router(other_handler.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())