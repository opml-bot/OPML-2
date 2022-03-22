from typing import Optional, Callable
import numpy as np
import pandas as pd


class Brandt:
    """
        Класс для решения задачи поиска минимума одномерной функции на отрезке комбинированным методом Брента.
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

    def __init__(self, func: Callable,
                 interval_x: tuple,
                 acc: Optional[float] = 10**-5,
                 max_iteration: Optional[int] = 500,
                 print_interim: Optional[bool] = False,
                 save_iters_df: Optional[bool] = False):
        self.func = func
        self.interval_x = interval_x
        self.acc = acc
        self.max_iteration = max_iteration
        self.print_interim = print_interim
        self.save_iters_df = save_iters_df

    def solve(self):
        """
        Метод решает созданную задачу.

        Returns
        ---------
        ans: str
            Строка с ответом в виде сообщения о причине остановки алгоримта (достигнута точность или максимальное число итераций)
            и ифномация об итерациях, есди флаг print_interim = True.
        """
        # инициализация начальных значений
        t = 10**-8
        if self.save_iters_df:
            df = pd.DataFrame(columns = ['u', 'Method'])

        a, b = self.interval_x
        C = (3 - 5**0.5)/2
        x0 = a + C*(b - a)
        x1 = x2 = x0
        d = e = 0
        f0 = f1 = f2 = self.func(x0)
        ans = ''

        # начало алгоритма
        for i in range(self.max_iteration):

            m = 0.5 * (a + b)
            tol = self.acc*abs(x0) + t
            t2 = 2*tol


            # критерий остановки
            if abs(x0 - m) <= t2 - 0.5*(b - a):
                break

            r = 0
            q = r
            p = q

            if tol < abs(e):
                r = (x0 - x1)*(f0 - f2)
                q = (x0 - x2)*(f0 - f1)
                p = (x0 - x2)*q - (x0 - x1)*r
                q = 2*(q - r)
                if 0 < q:
                    p = -p
                q = abs(q)
                r = e
                e = d

            if abs(p) < abs(0.5*q*r) and q*(a - x0) < p and p < q * (b - x0):
                # Шаг методом парабол
                method = 'Parabola'
                d = p/q
                u = x0 + d

                # Значения функции не должны быть очень близки к границам интервала
                if (u - a) < t2 or (b - u) < t2:
                    if x0 < m:
                        d = tol
                    else:
                        d = -tol
            else:
                # Шаг методом золотого сечения
                method = 'Golden'
                if x0 < m:
                    e = b - x0
                else:
                    e = a - x0
                d = C*e

                # Новая функция не должна быть слишком близка к x0
                if tol <= abs(d):
                    u = x0 + d
                elif 0 < d:
                    u = x0 + tol
                else:
                    u = x0 - tol

            fu = self.func(u)

            if fu <= f0:

                if u < x0:
                    if b != x0:
                        b = x0
                else:
                    if a != x0:
                        a = x0

                x2 = x1
                f2 = f1
                x1 = x0
                f1 = f0
                x0 = u
                f0 = fu

            else:
                if u < x0:
                    if a != u:
                        a = u
                else:
                    if b != u:
                        b = u

                if fu <= f1 or x1 == x0:
                    x2 = x1
                    f2 = f1
                    x1 = u
                    f1 = fu
                elif fu <= f2 or x2 == x0 or x2 == x1:
                    x2 = u
                    f2 = fu
            if self.save_iters_df:
                df = df.append({'u': u, 'Method': method}, ignore_index=True)
            if self.print_interim:
                ans = ans + f'iter: {i+1:>4} x: {x0:>.10f} method: {method:^10s}\n'
        else:
            ans = ans + f"Достигнуто максимальное число итераций. \nПолученная точка: {(x0, f0)}"
            if self.save_iters_df:
                return ans, df
            return ans
        ans = ans + f"Достигнута заданная точность. \nПолученная точка: {(x0, f0)}"
        if self.save_iters_df:
            return ans, df
        return ans


if __name__ == '__main__':
    func = [lambda x: -5*x**5 + 4*x**4 - 12*x**3 + 11*x**2 - 2*x + 1,
            lambda x: np.log(x-2)**2 + np.log(10 - x)**2 - x**0.2,
            lambda x: -3*x*np.sin(0.75*x) + np.exp(-2*x)]
    lims = [(-0.5, 0.5), (6, 9.9), (0, 2*np.pi)]

    j = 0
    x = Brandt(func[j], lims[j], max_iteration=100, acc =10**-5, save_iters_df=True)
    c = x.solve()
    desired_width = 320

    pd.set_option('display.width', desired_width)
    pd.set_option('display.max_columns', 12)
    print(c[0])
    print(c[1])
