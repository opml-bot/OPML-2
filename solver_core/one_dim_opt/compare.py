import pandas as pd
import numpy as np
import re

from parabola import Parabola
from bfgs import BFGS
from brandt import Brandt
from golden_ratio import GoldenRatio
from time import time


def get_point(s):
    point = s.split()[-2:]
    x, y = [float(re.sub(f'[\(\),]', '', i)) for i in point]
    return x, y


def alg_stat(alg, func, lims, start_point=0, **kwargs):
    alg_dict = {Parabola: 'Parabola',
                GoldenRatio: 'Golden Ratio',
                Brandt: 'Brent',
                BFGS: 'BFGS'}
    if alg_dict[alg] in ['Parabola', 'Golden Ratio', 'Brent', 'BFGS']:

        try:
            start = time()
            alg_ans = alg(func, lims).solve()
            working_time = start - time()
            point = get_point(alg_ans)
        except:
            point = (None, None)
            working_time = 0
    else:
        try:
            start = time()
            alg_ans = alg(func, start_point).solve()
            working_time = start - time()
            point = get_point(alg_ans)
        except:
            point = (None, None)
            working_time = 0
    d = {'Алгоритм': alg_dict[alg], 'x': point[0], 'y': point[1], 'Время работы': working_time}
    return d


def compare_alg(function, limits, started_point, **kwargs):

    all_algs_info = pd.DataFrame(columns=['Алгоритм', "x", 'y', "Время работы"])
    algs = [Parabola, GoldenRatio, Brandt, BFGS]
    for i in algs:
        info = alg_stat(function, limits, started_point)
        all_algs_info = all_algs_info.append(info, ignore_index=True)

if __name__ == '__main__':
    func = [lambda x: -5 * x ** 5 + 4 * x ** 4 - 12 * x ** 3 + 11 * x ** 2 - 2 * x + 1,
            lambda x: np.log(x - 2) ** 2 + np.log(10 - x) ** 2 - x ** 0.2,
            lambda x: -3 * x * np.sin(0.75 * x) + np.exp(-2 * x),
            lambda x: (x - 2) ** 2]
    lims = [(-0.5, 0.5), (6, 9.9), (0, 2 * np.pi), (-4, 4)]
    points = [0, 7, 1, 3]

    j = 3
    c = compare_alg(GoldenRatio, func[j], lims[j])
    print(c)
