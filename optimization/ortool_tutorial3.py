#-*- coding:utf-8 -*-
# Author : JoSp90, chofchof
# Date : 2018.01.22.
# reference : https://github.com/google/or-tools/issues/565

import numpy as np
from scipy import special, stats
from scipy.optimize import linprog
from scipy import integrate
from scipy.linalg import eig
from scipy.sparse.linalg import eigsh
import math

from ortools.linear_solver import pywraplp

def build_solve_milp(D, c, p, g):
    solver = pywraplp.Solver('MILP',pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    k = len(D)
    D = D.astype('d')
    r = {}
    m = {}
    b = {}
    const_r_y = {}
    const_y_m_b = {}
    const_m_b = {}
    y = solver.NumVar(0.0, solver.infinity(), 'y')
    for i in range(k):
        r[i] = solver.NumVar(0.0, D[i], 'r' + str(i))
        m[i] = solver.NumVar(0.0, solver.infinity(), 'm'+str(i))
        # b[i] = solver.IntVar(0.0, 1.0, 'b' + str(i))
        b[i] = solver.BoolVar('b'+str(i))
    M = np.max(D)
    cr = np.repeat(p/k, k)
    cm = np.repeat(g/k, k)
    solver.Maximize(-c*y +solver.Sum([cr[i]*r[i] for i in range(k)]) + solver.Sum([cm[i]*m[i] for i in range(k)]))
    for i in range(k):
        const_r_y[i] = solver.Add(-y + b[i]*r[i]<=0, 'const_r_y' + str(i))
        const_y_m_b[i] = solver.Add(-y + m[i] + b[i]*M <= -D[i] + M, 'const_y_m_b' + str(i))
        const_m_b[i] = solver.Add(m[i] - M*b[i] <= 0, 'const_m_b' + str(i))
    solver.Solve()
    y = y.SolutionValue()
    obj = -c*y + sum([cr[i]*min(y, D[i]) + cm[i]*max(y-D[i], 0) for i in range(len(D))])
    return y, obj


if __name__ == '__main__':
    c = 6
    p = 12
    g = 1
    D = np.array([60, 118, 114, 79, 97, 59, 76, 108, 96, 115])

    print(build_solve_milp(D, c, p, g))