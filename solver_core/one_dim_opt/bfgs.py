from typing import Optional, Callable
import numpy as np
import pandas as pd
from scipy.optimize import line_search


class BFGS:
    """
        Класс для решения задачи поиска минимума одномерной функции алгоритмом Бройдена — Флетчера — Гольдфарба — Шанно.
        BFGS
        Parameters
        ----------
        func : Callable
            Функция, у которой надо искать минимум.
        x0 : Sequence[float],
            Начальная точка
        c1: Optional[float] = 1e-4,
            Первая константа Вольфе. Обычно константа с1 выбирается достаточно маленькой (в окрестности 0)
        c2: Optional[float] = 1e-1,
            Вторая константа Вольфе. c2 выбирается значительно большей (в окрестности 1)
        max_arg: Optional[float] = 100
            Максимальное значение аргумента функции
        acc: Optional[float] = 1e-8
            Порог выхода по длине интервала поиска
        max_iteration: Optional[float] = 500,
            Максимально допустимое количество итераций. По умолчанию 500.
        print_interim: Optional[bool] = False
        Флаг, нужно ли сохранять информацию об итерациях. Информация записывается в \
            строку с ответом.
        save_iters_df: Optional[bool] = False
            Флаг, нужно ли сохранять информацию об итерациях в pandas.DataFrame
    """

    def __init__(self, func: Callable,
                 x0: np.ndarray,
                 c1: float = 1e-8,
                 c2: float = 0.99,
                 max_arg: float = 100,
                 acc: float = 1e-8,
                 max_iteration: float = 500,
                 print_interim: bool = False,
                 save_iters_df: bool = False):
        self.func = func
        self.x0 = np.array(x0, dtype=float)
        self.c1 = c1
        self.c2 = c2
        self.max_arg = max_arg
        self.acc = acc
        self.max_iteration = max_iteration
        self.print_interim = print_interim
        self.save_iters_df = save_iters_df
        self.x_ = 0
        self.y_ = 0

    def solve(self):
        """
        Метод решает созданную задачу.
        Returns
        ---------
        ans: str
            Строка с ответом в виде сообщения о причине остановки алгоримта
            (достигнута точность или максимальное число итераций)
            и информация об итерациях, есди флаг print_interim = True.
        """
        x_k = np.array(self.x0).reshape(-1, 1)
        h_k = np.eye(len(x_k)) * self.acc ** 0.5
        grad_f_k = gradient(self.func, x_k).reshape(-1, 1)
        f_k = self.func(x_k)

        answer = ''
        iterations_df = pd.DataFrame(columns=['x', 'y'])
            
        for k in range(self.max_iteration):
            if self.print_interim:
                answer += f"iter: {k + 1}\tx: {x_k[0, 0]:.12f}\ty: {f_k[0]:.12f}\n"
            if self.save_iters_df:
                iterations_df = iterations_df.append({'x': x_k, 'y': f_k}, ignore_index=True)
                
            if norm2(grad_f_k) < self.acc:
                self.x_ = x_k.reshape(-1)
                self.y_ = f_k.reshape(-1)
                answer = answer + f"Достигнута заданная точность. \nПолученная точка: {(self.x_[0], self.y_[0])}"
                return answer

            p_k = -h_k @ grad_f_k

            alpha_k = line_search(self.func, lambda x: gradient(self.func, x).reshape(1, -1), x_k, p_k,
                                  c1=self.c1, c2=self.c2, maxiter=self.max_iteration)[0]
            if alpha_k is None:
                self.x_ = x_k.reshape(-1)
                self.y_ = f_k.reshape(-1)
                answer += f"Константа alpha не находится. Метод не сошелся. \nПолученная точка: {(self.x_[0], self.y_[0])}"
                return answer

            x_k_plus1 = x_k + alpha_k * p_k
            grad_f_k_plus1 = gradient(self.func, x_k_plus1)
            s_k = x_k_plus1 - x_k
            y_k = grad_f_k_plus1 - grad_f_k

            h_k = calc_h_new(h_k, s_k, y_k)
            grad_f_k = grad_f_k_plus1
            x_k = x_k_plus1
            f_k = self.func(x_k)
            self.x_ = x_k.reshape(-1)
            self.y_ = f_k.reshape(-1)

        answer = answer + f"Достигнуто максимальное число итераций. \nПолученная точка: {(self.x_[0], self.y_[0])}"
        return answer


def gradient(func: Callable,
             x0: np.ndarray,
             delta_x=1e-8) -> np.ndarray:
    """
    Возращает градиент функии в точке x0
    Parameters
    ----------
    func : Callable
        Функция, у которой надо вернуть градиент.
    x0: np.ndarray
        Точка, в которой нужно найти градиент
    delta_x: Optional[float]
        величина приращения

    Returns
    ---------
    ans: Sequence[float]
        Список значений градиента в точках
    """
    grad = []
    for i in range(len(x0)):
        delta_x_vec_plus = x0.copy()
        delta_x_vec_minus = x0.copy()
        delta_x_vec_plus[i] += delta_x
        delta_x_vec_minus[i] -= delta_x
        grad_i = (func(delta_x_vec_plus) - func(delta_x_vec_minus)) / (2 * delta_x)
        grad.append(grad_i)

    grad = np.array(grad)
    return grad


def norm2(vec: np.ndarray) -> float:
    """
    Возращает l2 норму
    Parameters
    ----------
    vec: np.ndarray
        Массив, у которого требуется найти норму

    Returns
    ---------
    ans: float
        Норма вектора
    """
    vec = np.array(vec)
    return sum(vec ** 2) ** 0.5


def calc_h_new(h: np.ndarray,
               s: np.ndarray,
               y: np.ndarray) -> np.ndarray:
    """
    Считает новое приближение обратного Гессиана по методу BFGS
    Parameters
    ----------
    h: np.ndarray
        Предыдущее приближение матрицы H
    s: np.ndarray
        Вектор x_k+1 - x_k
    y: np.ndarray
        Вектор f'_k+1 - f'_k

    Returns
    ---------
    h: np.ndarray
        Следующее приближение матрицы H
    """
    ro = 1 / (y.T @ s)
    i = np.eye(h.shape[0])

    h_new = (i - ro * s @ y.T) @ h @ (i - ro * s @ y.T) + ro * s @ s.T
    return h_new


if __name__ == '__main__':
    def func1(x):
        return - x[0] / (x[0] ** 2 + 2)

    def func2(x):
        return (x[0] + 0.004) ** 5 - 2 * (x[0] + 0.004) ** 4

    def phi(alpha):
        if alpha <= 1 - 0.01:
            return 1 - alpha
        elif 1 - 0.01 <= alpha <= 1 + 0.01:
            return 1 / (2 * 0.01) * (alpha - 1) ** 2 + 0.01 / 2
        else:
            return alpha - 1

    def func3(x):
        return phi(x[0]) + 2 * (1 - 0.01) / (39 * np.pi) * np.sin(39 * np.pi / 2 * x[0])

    funcs = [func1, func2, func3]

    for j in range(3):
        x_solve = BFGS(funcs[j], 3, max_iteration=100, acc=10 ** -5, print_interim=True)
        c = x_solve.solve()
        print(c)
