from __future__ import annotations

from typing import Optional, Callable, Any
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class Parabola:
    """
    Класс для решения задачи поиска минимума одномерной функции на отрезке методом парабол.

    Parameters
    ----------
    func : Callable
        Функция, у которой надо искать минимум.
    interval_x : tuple
        Кортеж с двумя значениями типа float, которые задают ограничения для отрезка.
    acc: Optional[float] = 10**-5
        Точность оптимизации. Выражается как разница иксов на n и n-1 итерации.
        По умолчанию 10**-5
    max_iteration: Optional[int] = 500
        Максимально допустимое количество итераций. По умолчанию 500.
    print_interim: Optional[bool] = False
        Флаг, нужно ли сохранять информацию об итерациях. Информация записывается в
        строку с ответом.
    save_iters_df: Optional[bool] = False
        Флаг, нужно ли сохранять информацию об итерациях в pandas.DataFrame.
        Если фдаг стоит True, то этот датафрейм будет также возвращаться в методе
        solve.
    """

    def __init__(self,
                 func: Callable,
                 interval_x: tuple,
                 acc: Optional[float] = 10 ** -5,
                 max_iteration: Optional[int] = 500,
                 print_interim: Optional[bool] = False,
                 save_iters_df: Optional[bool] = False,
                 draw_flag: Optional[bool] = False):
        self.func = func
        self.interval_x = interval_x
        self.acc = acc
        self.max_iteration = max_iteration
        self.print_interm = print_interim
        self.save_iters_df = save_iters_df
        self.draw_flag = draw_flag

    def solve(self) -> str:
        """
        Метод решает задачу.

        Returns
        -------
        ans: str
            Строка с ответом и причиной остановки. Содержит информацию об итерациях при print_interm=True

        iterations_df: pandas.DataFrame
            Датафрейм с информацией об итерациях. Будет возвращен только если флаг save_iters_df = True

        """

        x2 = (self.interval_x[1] - self.interval_x[0]) * np.random.random() + self.interval_x[0]
        self.x = [self.interval_x[0], x2, self.interval_x[1]]
        self.y = [self.func(i) for i in self.x]
        self.x_ = None
        answer = ''
        if self.save_iters_df:
            iterations_df = pd.DataFrame(columns=['x', 'y'])
        if self.draw_flag:
            draw_df = pd.DataFrame(columns=['x', 'y', 'iter', 'size', 'color'])

        for i in range(self.max_iteration):
            last_x = self.x_
            self.x_ = self.count_new_x()
            if not self.x_:
                answer += f'В ходе вычислений произошла ошибка на {i+1} итерации. \nПоследняя точка: {last_x}'
            self.y_ = self.func(self.x_)
            if self.print_interm:
                answer += f"iter: {i + 1:<4d} x: {self.x_:.12f} y: {self.y_:.12f}\n"
            if self.save_iters_df:
                iterations_df = iterations_df.append({'x': self.x_, 'y': self.y_}, ignore_index=True)
            if self.draw_flag:
                d = pd.DataFrame({'x': self.x, 'y': self.y, 'iter': [i]*3, 'size': [10.0]*3, 'color': ['green', 'purple', 'blue']})
                draw_df = draw_df.append(d, ignore_index=True)
            if i == 0:
                story = self.x_
            else:
                if abs(self.x_ - story) <= self.acc:
                    answer = answer + f"Достигнута заданная точность. \nПолученная точка: {(self.x_, self.y_)}"
                    break
                story = self.x_
            intervals = self.new_interval()
            if not intervals:
                return 'Похоже, на отрезке нет минимума'
            self.x = intervals[0]
            self.y = intervals[1]
        else:
            answer = answer + f"Достигнуто максимальное число итераций. \nПолученная точка: {(self.x_, self.y_)}"
        if self.save_iters_df:
            if self.draw_flag:
                self.draw(draw_df)
            return answer, iterations_df
        else:
            return answer

    def count_new_x(self) -> float:
        """
        Метод вычисляет точкку минимума у параболы при заданных трёх точках.

        Returns
        -------
        float
            Вычисленное по формуле значение.
        """

        a1 = (self.y[1] - self.y[0]) / (self.x[1] - self.x[0])
        a2 = 1 / (self.x[2] - self.x[1]) * ((self.y[2] - self.y[0]) / (self.x[2] - self.x[0]) -
                                            (self.y[1] - self.y[0]) / (self.x[1] - self.x[0]))
        if a2 == 0:
            return False
        x = 1 / 2 * (self.x[0] + self.x[1] - a1 / a2)
        return x

    def new_interval(self):  # -> tuple[list[float | Any], list[Any]] | bool:
        """
        Метод определяет новые точки для итерации.

        Returns
        -------
        tuple[list[float | Any], list[Any]] | bool
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
        return False

    def draw(self, df):
        fig = px.scatter(df, x='x', y='y', animation_frame='iter',
                         range_x=[min(df['x']) - (max(df['x']) - min(df['x'])) * 0.15,
                                  max(df['x']) + (max(df['x']) - min(df['x'])) * 0.15],
                        range_y=[min(df['y']) - (max(df['y']) - min(df['y'])) * 0.15,
                                  max(df['y']) + (max(df['y']) - min(df['y'])) * 0.15],
                         size='size', color='color')
        func_x = np.linspace(self.interval_x[0], self.interval_x[1], 1000)
        func_y = [self.func(i) for i in func_x]
        fig.add_trace(go.Scatter(x=func_x, y=func_y))
        fig.update_layout(showlegend=False)
        fig.show()


if __name__ == "__main__":
    f = lambda x: -5 * x ** 5 + 4 * x ** 4 - 12 * x ** 3 + 11 * x ** 2 - 2 * x + 1  # -0.5 0.5
    task = Parabola(f, (-0.5, 0.5), print_interim=False, save_iters_df=True, draw_flag=True)
    res = task.solve()
    print(res[1])
