import numpy as np
from src import dao as dao
from src import rate as rate
from src.storage import Storage

import numpy as np
from scipy import special, stats
from scipy.optimize import linprog
from scipy import integrate
from scipy.linalg import eig
from scipy.sparse.linalg import eigsh
import math
from ortools.linear_solver import pywraplp


def build_solve_milp(load, pv, cost, r_nbc_m, r_on_m, r_mid_m, r_off_m, c_whole):
    # load, pv, cost는 365 * 96 짜리 1열로 dissolved
    solver = pywraplp.Solver('MILP', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    # Constant






load = dao.getRawLoad()
pv = dao.getRawPV()
es = dao.getRawES()
net = dao.getRawNet()


print("hi")