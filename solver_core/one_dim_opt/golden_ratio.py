from typing import Optional, Callable, Tuple
from numbers import Real, Integral
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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
      Точность оптимизации. Выражается как разница иксов на n и n-1 итерации.
      По умолчанию 10**-5
    max_iteration: Optional[int] = 500
      Максимально допустимое количество итераций. По умолчанию 500.
    print_interim: Optional[bool] = False
      Флаг, нужно ли сохранять информацию об итерациях. Информация записывается в
      строку с ответом.
    save_iters_df: Optional[bool] = False
      Флаг, нужно ли сохранять информацию об итерациях в pandas.DataFrame.
      Этот датафрейм будет возвращаться в методе solve, если этот флаг True.
    """

    def __init__(self, func: Callable[[Real], Real],
                 interval_x: Tuple,
                 acc: Optional[Real] = 10 ** -5,
                 max_iteration: Optional[Integral] = 500,
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
        Метод решает задачу c помощью золотого сечения
        Returns
        -------
        ans: str
            Строка с ответом и причиной остановки. Содержит информацию об итерациях при
            print_interm=True

        iters_df: pandas.DataFrame
            Датафрейм с информацией об итерации. Будет возвращен только если save_iters_df = True
        """

        phi: Real = (1 + 5 ** 0.5) / 2

        a: Real = self.interval_x[0]
        b: Real = self.interval_x[1]
        if self.save_iters_df:
            iters_df = pd.DataFrame(columns=['x', 'y'])
        if self.draw_flag:
            draw_df = pd.DataFrame(columns=['x', 'y', 'iter', 'size', 'color'])
            draw_df['iter'] = draw_df['iter'].astype(int)
            draw_df['size'] = draw_df['size'].astype(float)
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
            if self.draw_flag:
                d = {'x': [a, self.x_, b],
                                          'y': [self.func(a), self.y_, self.func(b)],
                                          'iter': [i]*3,
                                          'size': [10.0]*3,
                                          'color': ['red', 'blue', 'green']}
                draw_df = pd.concat([draw_df, pd.DataFrame(d)])
            if self.print_interm:
                answer += f"iter: {i + 1} x: {self.x_:.12f} y: {self.y_:.12f}\n"
            if self.save_iters_df:
                iters_df = iters_df.append({'x': self.x_, 'y': self.y_}, ignore_index=True)


            if abs(x1 - x2) < self.acc:
                answer += f"Достигнута заданная точность. \nПолученная точка: {(self.x_, self.y_)}"
                if self.save_iters_df:
                    if self.draw_flag:
                        a = self.draw(draw_df)
                        return answer, iters_df, a
                    else:
                        return answer, iters_df
                elif self.draw_flag:
                    a = self.draw(draw_df)
                    return answer, a
                return answer
        else:
            answer = answer + f"Достигнуто максимальное число итераций. \nПолученная точка: {(self.x_, self.y_)}"
            if self.save_iters_df:
                return answer, iters_df
            return answer

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
        return fig


if __name__ == "__main__":
    f = lambda x: -5 * x**5 + 4 * x**4 - 12 * x**3 + 11 * x**2 - 2 * x + 1  # -0.5 0.5
    task = GoldenRatio(f, (-0.5, 0.5), print_interim=False, save_iters_df=False, draw_flag=True)
    res = task.solve()
    res[1].show()
