from vk_bot.database import BotDatabase
from vk_bot.sql_queries import Select, Insert, Update


class OneDimOpt:
    def __init__(self, db: BotDatabase, user_id: int):
        self.db = db
        self.user_id = user_id

    def get_step(self) -> str:
        """
        Извлечение шага, на котором находится пользователь при решении задачи.

        Returns
        -------
        str
            Шаг, на котором находится пользователь, для решения задачи.
        """

        if not self.db.select(Select.ONEDIMOPT_STEP, (self.user_id,)):
            self.registration()
        return self.db.select(Select.ONEDIMOPT_STEP, (self.user_id,))[0]

    def registration(self):
        """
        Регистрация пользователя в базе данных в таблице onedimopt.
        """

        self.db.insert(Insert.ONEDIMOPT, (self.user_id,))