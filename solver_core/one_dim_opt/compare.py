import pandas as pd
import numpy as np
import re

from .parabola import Parabola
from .brandt import Brandt
from .golden_ratio import GoldenRatio
from .time import time


def get_point(s):
    """
    Функция достает из строки ответа числовые значения точки.

    Parameters
    ----------
    s: str
        Строка с выводом результат алгоритма.

    Returns:
    -------
    x, y: float
        Значение точки, полученной во время работы алгоритма
    """

    point = s.split()[-2:]
    x, y = [float(re.sub(f'[\(\),]', '', i)) for i in point]
    return x, y


def alg_stat(alg, func, lims,  a, max_iterat):
    """
    Функция собирает статистику для полученного алгоритма на полученных данных.

    Parameters
    ----------
    alg: object
        Класс, один из трех для этой задачи (Параболы, Золотое сечение или Брент)
    func: Callable
        Функция для оптимизации.
    lims: tuple/list
        Границы оптимизации. Задаются парой чисеол типа float
    a: float
        Параметр, задающий точность поиска минимума для решения.
    max_iterat: int
        Задает максимальное число итераций для поиска минимума.

    Returns:
    -------
    d: dict
        Словарь с необходимыми данными о работе алгоритма.

    """
    alg_dict = {Parabola: 'Parabola',
                GoldenRatio: 'Golden Ratio',
                Brandt: 'Brent'}
    if alg_dict[alg] in ['Parabola', 'Golden Ratio', 'Brent']:
        try:
            start = time()
            alg_ans = alg(func, lims, save_iters_df=True, acc=a, max_iteration=max_iterat).solve()
            working_time = time() - start
            point = get_point(alg_ans[0])
            n_iters = alg_ans[1].shape[0]
        except:
            point = (None, None)
            working_time = 0
            n_iters = -1
    d = {'Алгоритм': alg_dict[alg], 'x': point[0], 'y': point[1], 'Время работы': working_time, 'Число итераций': n_iters}
    return d


def compare_alg(function, limits, acc=10**-5, max_iter=100):
    """Функция строит датафрейм для сравнения работы трех алгоритмов.
    В случае ошибки в работе, выдает точку как None, а число итераций = -1.

    Parameters
    ----------
    function: Callable
        Функция, которую надо минимизировать.
    limits: tuple/list
        Массив, содержащий два числа, которые определяют границы оптимизации.
    acc: Optional[float] = 10**-5
        Точность оптимизации
    max_iter: Optional[int] = 100
        Максимальное число итераций алгоритмов.

    Returns:
    -------
    all_algs_info: pandas.DataFrame
        Датафрейм со статисткой работы алгоритмов
    """

    all_algs_info = pd.DataFrame(columns=['Алгоритм', "x", 'y', "Время работы"])
    algs = [Parabola, GoldenRatio, Brandt]
    for i in algs:
        info = alg_stat(i, function, limits, acc, max_iter)
        all_algs_info = all_algs_info.append(info, ignore_index=True)
    return all_algs_info

if __name__ == '__main__':
    func = [lambda x: -5 * x ** 5 + 4 * x ** 4 - 12 * x ** 3 + 11 * x ** 2 - 2 * x + 1,
            lambda x: np.log(x - 2) ** 2 + np.log(10 - x) ** 2 - x ** 0.2,
            lambda x: -3 * x * np.sin(0.75 * x) + np.exp(-2 * x),
            lambda x: (x - 2) ** 2]
    d = {'acc': 10**-8, 'max_iter': 1000}
    lims = [(-0.5, 0.5), (6, 9.9), (0, 2 * np.pi), (-4, 4)]
    points = [0, 7, 1, 3]

    j = 1
    c = compare_alg(func[j], lims[j],  acc=10**-8, max_iter=1000)
    print(c)
