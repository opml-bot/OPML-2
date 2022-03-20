from vk_bot.database import BotDatabase
from vk_bot.sql_queries import Select, Insert, Update


class OneDimOpt:
    def __init__(self, db: BotDatabase, user_id: int):
        self.db = db
        self.user_id = user_id

    def registration(self):
        """
        Регистрация пользователя в базе данных в таблице onedimopt.
        """

        self.db.insert(Insert.ONEDIMOPT, (self.user_id,))

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

    def get_type(self) -> str:
        """
        Извлечение типа задачи, которая задается пользователем.

        Returns
        -------
        str
            Тип задачи, которая задается пользователем.
        """

        return self.db.select(Select.ONEDIMOPT_TYPE, (self.user_id,))[0]

    def get_params(self) -> str:
        """
        Извлечение всех внесенных данных для передачи их в реализацию алгоритма.

        Returns
        -------
        str
            Все данные, необходимые для решения задачи.
        """

        # TODO: написать реализацию метода
        pass

    def update_step(self, step: str):
        """
        Изменение шага, на котором находится пользователь, в базе данных.

        Parameters
        ----------
        step : str
            Новый шаг, который будет записан в базу данных.
        """

        self.db.update(Update.ONEDIMOPT_STEP, (step, self.user_id))

    def update_type(self, task_type: str):
        """
        Изменение типа задачи в базе данных.

        Parameters
        ----------
        task_type : str
            Тип задачи, который будет записан в базу данных.
        """

        self.db.update(Update.ONEDIMOPT_TYPE, (task_type, self.user_id))

    def update_func(self, func: str):
        """
        Изменение функции в базе данных.

        Parameters
        ----------
        func : str
            Функция, которая будет записана в базу данных.
        """

        self.db.update(Update.ONEDIMOPT_FUNC, (func, self.user_id))

    def update_acc(self, acc: float):
        """
        Изменение целевой точности для алгоритма в базе данных.

        Parameters
        ----------
        acc : float
            Целевая точность для алгоритма, которая будет записана в базу данных.
        """

        self.db.update(Update.ONEDIMOPT_ACC, (acc, self.user_id))

    def update_max_iter(self, max_iter: int):
        """
        Изменение максимального количества итераций алгоритма в базе данных.

        Parameters
        ----------
        max_iter : int
            Максимальное количество итераций алгоритма, которое будет записано в базу данных.
        """

        self.db.update(Update.ONEDIMOPT_MAX_ITER, (max_iter, self.user_id))

    def update_print_interim(self, print_interim: int):
        """
        Изменение флага вывода промежуточных результатов в базе данных.

        Parameters
        ----------
        print_interim : int
            Флаг вывода промежуточных результатов, который будет записан в базу данных.
        """

        self.db.update(Update.ONEDIMOPT_PRINT_INTERIM, (print_interim, self.user_id))
