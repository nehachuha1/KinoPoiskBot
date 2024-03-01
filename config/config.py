from dataclasses import dataclass
from dotenv import dotenv_values
from database.database import Database, CacheDatabase

db = Database()
cached_db = CacheDatabase()

@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    
@dataclass
class Config:
    tg_bot: TgBot

def load_config(path: str | None = None) -> Config:
    env_values = dotenv_values(path)
    return Config(tg_bot=TgBot(token=env_values['TOKEN'],
                               admin_ids=env_values['ADMIN_IDS']
                               ))