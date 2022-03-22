from vk_api.vk_api import VkApiMethod

from vk_bot.answerer.one_dim_opt.message_handlers import Handlers
from vk_bot.answerer.one_dim_opt.onedimopt import OneDimOpt
from vk_bot.answerer.response_init import Response
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
        self.onedimopt = OneDimOpt(db, user.user_id)
        self.step = self.onedimopt.get_step()
#         TODO: аттрибут type добавить при необходимости
        self.handlers = Handlers(vk_api_method, db, user)

    def manage(self, text: str) -> Response:
        """
        Управление обработкой входящих сообщений для ввода исходных данных в задаче.

        Parameters
        ----------
        text : str
            Текст сообщения, отправленного пользователем.

        Returns
        -------
        Response
            Сообщение для пользователя.
        """

        if self.step == 'start':
            return self.handlers.task_type_selection()