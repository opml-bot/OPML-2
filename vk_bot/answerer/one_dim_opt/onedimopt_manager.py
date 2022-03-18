from vk_api.vk_api import VkApiMethod

from vk_bot.answerer.one_dim_opt.message_handlers import Handlers
from vk_bot.database import BotDatabase
from vk_bot.user import User


class OneDimOptManager:
    """
    Менеджер управления решением задачи одномерной оптимизации.

    Parameters
    ----------
    vk_api_method : VkApiMethod
        Объект соединения с VK и набор методов API.
    db : BotDatabase
        Объект для взаимодействия с базой данных.
    user : User
        Объект для взаимодействия с данными пользователя.
    """

    def __init__(self, vk_api_method: VkApiMethod, db: BotDatabase, user: User):
        self.vk_api_method = vk_api_method
        self.db = db
        self.user = user
        self.handlers = Handlers(vk_api_method, db, user)
