from typing import Optional, Callable
import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar as check

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

    def __init__(self, func: Callable, interval_x: tuple, acc: Optional[float] = 10**-5, max_iteration: Optional[int] = 500,
                 print_interim: Optional[bool] = False, save_iters_df: Optional[bool] = False):
        self.func = func
        self.interval_x = interval_x
        self.acc = acc
        self.max_iteration = max_iteration
        self.print_interim = print_interim
        self.save_iters_df = save_iters_df

    def solve(self):
        # инициализация начальных значений
        t = 0
        df = pd.DataFrame(columns = ['u', 'Method'])
        a, b = self.interval_x
        c = (3 - 5**0.5)/2
        v = w = x = a + c * (b - a)
        e = 0
        fv = fw = fx = self.func(x)

        # начало алгоритма
        for i in range(self.max_iteration):
            m = 0.5 * (a + b)
            tol = self.acc * abs(x) + t
            t2 = 2 * tol

            # критерий остановки
            if abs(x - m) > t2 - 0.5*(b - a):
                p = q = r = 0

                if abs(e) > tol:
                    # вычмсления для метода парабол
                    r = (x - w)*(fx - fv)
                    q = (x - v)*q - (x-w)*r
                    q = 2*(q-r)
                    if q > 0:
                        p = -p
                    else:
                        q = -q
                    r = e
                    e = d

                if abs(p) < abs(0.5*q*r) and p < q * (a - x) and p < q*(b - x):
                    # выполняем шаг методом парабол
                    method = 'Parabola'
                    d = p/q
                    u = x + d
                    if u - a < t2 and b - u < t2:
                        if x < m:
                            d = tol
                        else:
                            d = -tol
                else:
                    # шаг методом золотого сечения
                    method = 'Golden'
                    if x < m:
                        e = b - x
                    else:
                        e = a - x
                    d = c*e

                if abs(d) >= tol:
                    u = x + d
                elif d > 0:
                    u = x + tol
                else:
                    u = x - tol
                fu = self.func(u)

                if fu <= fx:
                    if u < x:
                        b = x
                    else:
                        a = x
                    v = w
                    fv = fw
                    w = x
                    fw = fx
                    x = u
                    fx = fu
                else:
                    if u < x:
                        a = u
                    else:
                        b = u
                    if fu <= fv or v == x or v == w:
                        v = u
                        fv = fu
            else:
                return i+1, x, fx, df
            df = df.append({'u': u, 'Method': method}, ignore_index=True)
        return i+1, x, fx, df



    def parabola(self, p):
        """
        Метод вычисляет точкку минимума у параболы при заданных трёх точках.

        Parameters
        ----------
        p: list of tuples
            Список с кортежами, содержащие пары точек (x, y). Всего три точки.

        Returns
        -------
        x: float
            Вычисленное по формуле значение.
        """
        pass

    def update_parameters(self):
        """

        Returns
        -------

        """
        pass

if __name__ == '__main__':
    func = [lambda x: -5*x**5 + 4*x**4 - 12*x**3 + 11*x**2 - 2*x + 1,
            lambda x: np.log(x-2)**2 + np.log(10 - x)**2 - x**0.2,
            lambda x: -3*x*np.sin(0.75*x) + np.exp(-2*x)]
    lims = [(-0.5, 0.5), (6, 9.9), (0, 2*np.pi)]

    j = 2
    x = Brandt(func[j], lims[j], max_iteration=100, acc =10**-5)
    c = x.solve()
    desired_width = 320

    pd.set_option('display.width', desired_width)
    pd.set_option('display.max_columns', 12)
    # ans = check(func[j], method='brent', bounds=[lims[j]], tol=10**-5)
    # print(f'nit: {ans["nit"]:>4}, x: {ans["x"]}')
    print(f'nit: {c[0]:>4}, x: {c[1]}, f(x): {c[2]}')
    print(c[3])
