from vk_bot.database import BotDatabase
from vk_bot.sql_queries import Select, Insert, Update


class OneDimOpt:
    def __init__(self, db: BotDatabase, user_id: int):
        self.db = db
        self.user_id = user_id


