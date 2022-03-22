from typing import Optional, Callable, Tuple
from numbers import Real, Integral

import pandas as pd


class GoldenRatio:
    """
    Класс для решения задачи поиска минимума одномерной функции на отрезке методом парабол.

    Parameters
    ----------
    func : Callable
      Функция, у которой надо искать минимум.
    interval_x : tuple
      Кортеж с двумя значениями типа float, которые задают ограничения для отрезка.
    acc: Optional[float] = 10**-5
      Точность оптимизации. Выражается как разница иксов на n и n-1 итерации. \
      По умолчанию 10**-5
    max_iteration: Optional[int] = 500
      Максимально допустимое количество итераций. По умолчанию 500.
    print_interim: Optional[bool] = False
      Флаг, нужно ли сохранять информацию об итерациях. Информация записывается в \
      строку с ответом.
    save_iters_df: Optional[bool] = False
      Флаг, нужно ли сохранять информацию об итерациях в pandas.DataFrame
    """

    def __init__(self, func: Callable[[Real], Real],
                 interval_x: Tuple,
                 acc: Optional[Real] = 10 ** -5,
                 max_iteration: Optional[Integral] = 500,
                 print_interim: Optional[bool] = False,
                 save_iters_df: Optional[bool] = False):
        self.func = func
        self.interval_x = interval_x
        self.acc = acc
        self.max_iteration = max_iteration
        self.print_interm = print_interim
        self.save_iters_df = save_iters_df

    def solve(self) -> str:
        """
        Метод решает задачу c помощью золотого сечения
        Returns
        -------
        str
            Строка с ответом и причиной остановки. Содержит информацию об итерациях при \
            print_interm=True
        """

        phi: Real = (1 + 5 ** 0.5) / 2

        a: Real = self.interval_x[0]
        b: Real = self.interval_x[1]
        if self.save_iters_df:
            iters_df = pd.DataFrame(columns=['x', 'y'])
        answer = ''

        for i in range(1, self.max_iteration):
            x1: Real = b - (b - a) / phi
            x2: Real = a + (b - a) / phi

            if self.func(x1) > self.func(x2):
                a = x1
            else:
                b = x2
            self.x_ = (a + b) / 2
            self.y_ = self.func(self.x_)
            if self.print_interm:
                answer += f"iter: {i + 1} x: {self.x_:.12f} y: {self.y_:.12f}\n"
            if self.save_iters_df:
                iters_df = iters_df.append({'x': self.x_, 'y': self.y_}, ignore_index=True)


            if abs(x1 - x2) < self.acc:
                answer += f"Достигнута заданная точность. \nПолученная точка: {(self.x_, self.y_)}"
                if self.save_iters_df:
                    return answer, iters_df
                return answer
        else:
            answer = answer + f"Достигнуто максимальное число итераций. \nПолученная точка: {(self.x_, self.y_)}"
            if self.save_iters_df:
                return answer, iters_df
            return answer


if __name__ == "__main__":
    f = lambda x: -5 * x**5 + 4 * x**4 - 12 * x**3 + 11 * x**2 - 2 * x + 1  # -0.5 0.5
    task = GoldenRatio(f, (-0.5, 0.5), print_interim=False, save_iters_df=True)
    res = task.solve()
    print(res[1])
