from typing import Optional, Callable
import numpy as np
import pandas as pd

class Parabola:
    """
    Класс для решения задачи поиска минимума одномерной функции на отрезке методом парабол.

    Parameters
    ----------
    func : Callble
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

    def __init__(self, func: Callable, interval_x: tuple, acc: Optional[float] = 10**-5, max_iteration: Optional[int] = 500,
                 print_interim: Optional[bool] = False, save_iters_df: Optional[bool] = False):
        self.func = func
        self.interval_x = interval_x
        self.acc = acc
        self.max_iteration = max_iteration
        self.print_interm = print_interim
        self.save_iters_df = save_iters_df

    def solve(self):
        """
        Метод решает задачу.

        Returns
        -------
        ans: str
            Строка с ответом и причиной остановки. Содержит информацию об итерациях при \
            print_interm=True
        """

        x2 = (self.interval_x[1] - self.interval_x[0])*np.random.random() + self.interval_x[0]
        self.x = [self.interval_x[0], x2, self.interval_x[1]]
        self.y = [self.func(i) for i in self.x]
        answer = ''
        if self.save_iters_df:
            iterations_df = pd.DataFrame(columns=['x', 'y'])

        for i in range(self.max_iteration):
            self.x_ = self.count_new_x()
            self.y_ = self.func(self.x_)
            if self.print_interm:
                answer += f"iter: {i+1} x: {self.x_:.12f} y: {self.y_:.12f}\n"
            if self.save_iters_df:
                iterations_df = iterations_df.append({'x': self.x_, 'y': self.y_}, ignore_index=True)
            if i == 0:
                story = self.x_
            else:
                if abs(self.x_ - story) <= self.acc:
                    answer = answer + f"Достигнута заданная точность. \nПолученная точка: {(self.x_, self.y_)}"
                    break
                story = self.x_

            intervals = self.new_interval()
            self.x = intervals[0]
            self.y = intervals[1]
        else:
            answer = answer + f"Достигнуто максимальное число итераций. \nПолученная точка: {(self.x_, self.y_)}"
        return answer
    def count_new_x(self):
        """
        Метод вычисляет точкку минимума у параболы при заданных трёх точках.

        Returns
        -------
        x: float
            Вычисленное по формуле значение.
        """

        a1 = (self.y[1] - self.y[0]) / (self.x[1] - self.x[0])
        a2 = 1 / (self.x[2] - self.x[1]) * ((self.y[2] - self.y[0]) / (self.x[2] - self.x[0]) -
                                            (self.y[1] - self.y[0]) / (self.x[1] - self.x[0]))
        x = 1 / 2 * (self.x[0] + self.x[1] - a1 / a2)
        return x

    def new_interval(self):
        """
        Метод определяет новые точки для итерации.

        Returns
        -------
        x, y: list
            Значения новых точек и значения функции в них.
        """
        if self.x[0] <= self.x_ <= self.x[1]:
            if self.y_ > self.y[1]:
                return [self.x_, self.x[1], self.x[2]], [self.y_, self.y[1], self.y[2]]
            else:
                return [self.x[0], self.x_, self.x[1]], [self.y[0], self.y_, self.y[1]]
        if self.x[1] <= self.x_ <= self.x[2]:
            if self.y[1] > self.y_:
                return [self.x[1], self.x_, self.x[2]], [self.y[1], self.y_, self.y[2]]
            else:
                return [self.x[0], self.x[1], self.x_], [self.y[0], self.y[1], self.y_]


if __name__ == "__main__":
    f = lambda x: -5*x**5 + 4*x**4 - 12*x**3 + 11*x**2 - 2*x + 1 # -0.5 0.5
    task = Parabola(f, [-0.5, 0.5], print_interim=True, save_iters_df=True)
    res = task.solve()
    print(res)