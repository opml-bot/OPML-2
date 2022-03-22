from typing import Optional
from sympy.parsing.sympy_parser import parse_expr
from sympy import sympify, exp

ALLOWED_OPERATIONS = ['log', 'ln', 'factorial', 'sin', 'cos', 'tan', 'cot', 'pi', 'exp', 'sqrt', 'root']


def check_expression(expression: str) -> str:
    """
    Функция для проверки выражения на корректность. Принимает на вход строку с функцией
    в аналитическом виде, возвращает строку. Функция обязательно должна быть
    только от аргумента x

    Parameters:
    ------------
    expression: str
    Строка содержащая функцию для проверки.

    Returns:
    -------
    str
        Функция в виде строки.
    """

    expression = expression.strip()
    if expression.find('—') != -1:
        expression = expression.replace('—', '-')

    if expression.find('–') != -1:
        expression = expression.replace('–', '-')

    checker = compile(expression, '<string>', 'eval')  # Может выдать SyntaxError, если выражение некорректно

    for name in checker.co_names:
        if name not in ALLOWED_OPERATIONS and name != 'x':
            raise NameError(f"The use of '{name}' is not allowed")

    function = sympify(expression, {'e': exp(1)}, convert_xor=True)
    if len(function.free_symbols) != 1:
        raise ValueError('После парсинга функция не содержит переменных или содержит больше одной переменной')
    return str(function)


def check_limits(limits: str, split_by: Optional[str] = None) -> str:
    """
    Эта функция проверяет корректность введеных ограничений для переменных.
    Поддерживает операции с pi и e.

    Parameters:
    ------------
    limits: str
        Строка сожержащая ограничения слева и справа для переменной.
    split_by: Optional[str] = None
        Символ, которым разделяются ограничения.

    Returns:
    -------
    str
        Строка с ограничениями, разделенными пробелом.
    """

    if limits == 'None':
        return 'None'
    if limits.find('^') != -1:
        limits = limits.replace('^', '**')
    if limits.find('—') != -1:
        limits = limits.replace('—', '-')
    if limits.find('–') != -1:
        limits = limits.replace('–', '-')

    if len(limits.split(split_by)) != 2:
        raise ValueError('Неправильный формат ввода')
    else:
        limits = limits.split(split_by)

    float_lim = []
    for i in range(len(limits)):
        checker = compile(limits[i], '<string>', 'eval')  # Может выдать SyntaxError, если выражение некорректно
        for name in checker.co_names:
            if name not in ['pi', 'e', 'exp']:
                raise ValueError(f'Нельзя использовать имя {name}')

        k = parse_expr(limits[i], {'e': exp(1)}).evalf()
        float_lim.append(float(k))
    if float_lim[0] > float_lim[1]:
        raise ValueError('Левая граница превосходит правую')
    return f'{limits[0]} {limits[1]}'


def check_float(value: str) -> float:
    """
    Проверяет введеное значение на корректность и на наличие инъекций, а затем
    конвертирует в float, если это возможно. Поддерживает операции с pi и e.

    Parameters:
    ------------
    values: str
        строка в которой содержится выражение

    Returns:
    -------
    float
        значение переведенное из строки в float
    """
    if value.find('^') != -1:
        value = value.replace('^', '**')
    checker = compile(value, '<string>', 'eval')  # Может выдать SyntaxError, если выражение некорректно
    for name in checker.co_names:
        if name not in ['pi', 'e', 'exp']:
            raise ValueError(f'Нельзя использовать имя {name}')
    value = float(parse_expr(value, {'e': exp(1)}))
    return value


def check_int(value: str) -> int:
    """
    Проверяет введеное значение на корректность и на наличие инъекций, а затем
    конвертирует в int, если это возможно.

    Parameters:
    ------------
    values: str
        строка в которой содержится выражение

    Returns:
    -------
    int
        значение переведенное из строки в int
    """
    if value.find('^') != -1:
        value = value.replace('^', '**')
    value = int(parse_expr(value))
    return value


if __name__ == '__main__':
    print(check_limits("pi/2 pi/2"))
    print(check_expression('x+log(2, 2)'))
    print(check_float('10^-5'))
