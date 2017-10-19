#!/usr/bin/env python
from mosi.solver import CbcCliSolver, CplexCliSolver, GlpkCliSolver, LpSolveCliSolver


CBC_LP_SOLVER = CbcCliSolver("C:/Dev/CBC/2.9.7/x64/cbc.exe", "lp")
CBC_MPS_SOLVER = CbcCliSolver("C:/Dev/CBC/2.9.7/x64/cbc.exe", "mps")

CPLEX_LP_SOLVER = CplexCliSolver(file_type="lp")
CPLEX_MPS_SOLVER = CplexCliSolver(file_type="mps")

GLPK_LP_SOLVER = GlpkCliSolver("C:/Dev/GLPK/4.60/x64/glpsol.exe", "lp")
GLPK_MPS_SOLVER = GlpkCliSolver("C:/Dev/GLPK/4.60/x64/glpsol.exe", "mps")

LP_SOLVER_LP_SOLVER = LpSolveCliSolver("C:/Dev/LpSolve/5.5.2.5/x64/lp_solve.exe", "lp")
LP_SOLVER_MPS_SOLVER = LpSolveCliSolver("C:/Dev/LpSolve/5.5.2.5/x64/lp_solve.exe", "mps")


# noinspection PyShadowingBuiltins
class Problem:
    def __init__(self, model, vars):
        self.model = model
        self.vars = vars

    def clear(self):
        self.model.clear()
