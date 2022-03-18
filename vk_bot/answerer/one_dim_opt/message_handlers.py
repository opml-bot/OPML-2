from vk_api.vk_api import VkApiMethod

from vk_bot.answerer.response_init import Response
from vk_bot.database import BotDatabase
from vk_bot.user import User


class Handlers:
    """
    Генератор ответов пользователю.

    Parameters
    ----------
    vk_api_method : VkApiMethod
        Объект соединения с VK и набор методов API.
    db : BotDatabase
        Объект для взаимодействия с базой данных.
    user : User
        Объект для взаимодействия с данными пользователя.
    """

    def __init__(self, vk_api_method: VkApiMethod, db: BotDatabase, user: User, onedimopt: OneDimOpt):
        self.vk = vk_api_method
        self.db = db
        self.user = user
        self.onedimopt = onedimopt
        self.response = Response(self.user.user_id)
