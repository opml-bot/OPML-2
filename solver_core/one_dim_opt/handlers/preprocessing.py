from sympy.parsing.sympy_parser import parse_expr
from sympy import sympify, exp, Symbol, lambdify
from typing import Optional, Callable


def prepare_func(func: str) -> Callable:
    """
    Преобразует функцию записанной в строковом виде в функицю питона.

    Parameters:
    ------------
    func: str
        Функция в аналитическом виде, записанная в строке.

    Returns:
    -------
    function
        питоновская функция
    """

    x = Symbol('x')
    func = sympify(func)
    func = lambdify([x], func)
    return func


def prepare_limits(limits: str) -> tuple:
    """
    Преобразует строку с ограничениями в одномерный кортеж с двумя элементами типа float.
    Первый элемент - левая граница, второй - правая.
    Parameters:
    ------------
    limits: str
        Строка с ограничениями, разделенными пробелом.

    Returns:
    -------
    tuple
        одномерный кортеж длины 2 с значениями типа float
    """
    limits = limits.split()
    for i in range(len(limits)):
        limits[i] = float(parse_expr(limits[i], {'e': exp(1)}))
    limits = tuple(limits)
    return limits


if __name__ == '__main__':
    f = prepare_func('x**2 + x - 3')
    print(f(2))
    lims = prepare_limits('3*pi/2 e**2')
    print(lims)
