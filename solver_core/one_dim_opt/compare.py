import pandas as pd
import numpy as np

from parabola import Parabola
from bfgs import BFGS
from brandt import Brandt
from golden_ratio import GoldenRatio
from time import time

def compare_alg(func, lims, start_point):
    ans = []
    timers = []
    numbers = re.compile(f'[-0-9.]+')
    try:
        start= time()
        alg_ans = Parabola(func, lims).solve()
        working_time = start - time()
        print(alg_ans)
        alg_ans = numbers.findall(alg_ans)
        print(alg_ans)
        ans.append(alg_ans)
        timers.append(working_time)
    except:
        ans.append('Ошибка выполнения')
        timers.append(0)


    try:
        start = time()
        alg_ans = BFGS(func, start_point).solve()
        working_time = start - time()
        ans.append(alg_ans)
        timers.append(working_time)
    except:
        ans.append('Ошибка выполнения')
        timers.append(0)

    results = pd.DataFrame({'Алгоритм': ['Парабола', "Золотое сечение", "Брент", "BFGS"],
                            'Полученное значение': ans,
                            'Время работы': timers})
    return results


if __name__ == '__main__':
    func = [lambda x: -5*x**5 + 4*x**4 - 12*x**3 + 11*x**2 - 2*x + 1,
            lambda x: np.log(x-2)**2 + np.log(10 - x)**2 - x**0.2,
            lambda x: -3*x*np.sin(0.75*x) + np.exp(-2*x),
            lambda x: (x - 2)**2]
    lims = [(-0.5, 0.5), (6, 9.9), (0, 2*np.pi), (-4, 4)]
    points = [0, 7, 1, 3]

    j = 3
    c = compare_alg(func[j], lims[j], points[j])
    print(c)

