from vk_api.vk_api import VkApiMethod

from vk_bot.answerer.one_dim_opt.keyboards import Keyboards
from vk_bot.answerer.one_dim_opt.onedimopt import OneDimOpt
from vk_bot.answerer.one_dim_opt.scripted_phrases import Phrases
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

    def opt_alg_selection(self) -> Response:
        """
        Выбор алгоритма для оптимизации.
        Шаг: opt_alg_selection

        Returns
        -------
        Response
            Сообщение для пользователя.
        """
        self.onedimopt.update_step('opt_alg_selection')
        self.response.set_text(Phrases.OPT_ALG_SELECTION)
        self.response.set_keyboard(Keyboards().for_opt_alg_selection())
        return self.response

    def input_func(self) -> Response:
        """
        Предложение ввести функцию для оптимизации.
        Шаг: input_func

        Returns
        -------
        Response
            Сообщение для пользователя.
        """
        self.onedimopt.update_step('input_func')
        self.response.set_text(Phrases.INPUT_FUNC)
        return self.response

    def func(self) -> Response:
        """
        Обработка введенной функции. Предложение ввести точность оптимизации.

        Returns
        -------
        Response
            Сообщение для пользователя.
        """

        try:
            func = check_f
        except Exception as e:
            return self.error(e)



    def error(self, error: str) -> Response:
        """
        Отправка сообщения об ошибке.

        Parameters
        ----------
        error : str
            Описание ошибки.

        Returns
        -------
        Response
            Сообщение для пользователя.
        """
        self.response.set_text(Phrases.ERROR.format(error))
        return self.response
