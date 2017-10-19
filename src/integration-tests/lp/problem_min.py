#!/usr/bin/env python
from shutil import rmtree

from mosi.common import ModelStatus
from mosi.lp import Model, DecisionVariable

# noinspection PyPackageRequirements,PyUnresolvedReferences
from init import (
    CBC_LP_SOLVER, CBC_MPS_SOLVER, CPLEX_LP_SOLVER, CPLEX_MPS_SOLVER,
    GLPK_LP_SOLVER, GLPK_MPS_SOLVER, LP_SOLVER_LP_SOLVER, LP_SOLVER_MPS_SOLVER, Problem
)


DELETE = False
DIRECTORY = "../../../volume/results"
OBJECTIVE = 320
SOLUTION = [3.6, 1.4]
TOLERANCE = 10 ** -8


def setup():
    rmtree(DIRECTORY, True)

    model = Model()

    x = {1: DecisionVariable(model), 2: DecisionVariable(model)}

    model.min(
        50 * x[1] + 100 * x[2]
    )

    model.subject_to(
        7 * x[1] + 2 * x[2] >= 28,
        2 * x[1] + 12 * x[2] >= 24
    )

    return Problem(model, x.values())


def run_cbc_lp(problem):
    CBC_LP_SOLVER.solve(problem.model, directory=DIRECTORY, delete=DELETE)

    assert problem.model.get_objective().get_value() == OBJECTIVE
    assert all(abs(var.get_value() - sol) < TOLERANCE for var, sol in zip(problem.vars, SOLUTION))
    assert problem.model.get_status() == ModelStatus.OPTIMAL


def run_cbc_mps(problem):
    CBC_MPS_SOLVER.solve(problem.model, directory=DIRECTORY, delete=DELETE)

    assert problem.model.get_objective().get_value() == OBJECTIVE
    assert all(abs(var.get_value() - sol) < TOLERANCE for var, sol in zip(problem.vars, SOLUTION))
    assert problem.model.get_status() == ModelStatus.OPTIMAL


def run_cplex_lp(problem):
    CPLEX_LP_SOLVER.solve(problem.model, directory=DIRECTORY, delete=DELETE)

    assert problem.model.get_objective().get_value() == OBJECTIVE
    assert all(abs(var.get_value() - sol) < TOLERANCE for var, sol in zip(problem.vars, SOLUTION))
    assert problem.model.get_status() == ModelStatus.OPTIMAL


def run_cplex_mps(problem):
    CPLEX_MPS_SOLVER.solve(problem.model, directory=DIRECTORY, delete=DELETE)

    assert problem.model.get_objective().get_value() == OBJECTIVE
    assert all(abs(var.get_value() - sol) < TOLERANCE for var, sol in zip(problem.vars, SOLUTION))
    assert problem.model.get_status() == ModelStatus.OPTIMAL


def run_glpk_lp(problem):
    GLPK_LP_SOLVER.solve(problem.model, directory=DIRECTORY, delete=DELETE)

    assert problem.model.get_objective().get_value() == OBJECTIVE
    assert all(abs(var.get_value() - sol) < TOLERANCE for var, sol in zip(problem.vars, SOLUTION))
    assert problem.model.get_status() == ModelStatus.OPTIMAL


def run_glpk_mps(problem):
    GLPK_MPS_SOLVER.solve(problem.model, directory=DIRECTORY, delete=DELETE)

    assert problem.model.get_objective().get_value() == OBJECTIVE
    assert all(abs(var.get_value() - sol) < TOLERANCE for var, sol in zip(problem.vars, SOLUTION))
    assert problem.model.get_status() == ModelStatus.OPTIMAL


def run_lp_solve_lp(problem):
    LP_SOLVER_LP_SOLVER.solve(problem.model, directory=DIRECTORY, delete=DELETE)

    assert problem.model.get_objective().get_value() == OBJECTIVE
    assert all(abs(var.get_value() - sol) < TOLERANCE for var, sol in zip(problem.vars, SOLUTION))
    assert problem.model.get_status() == ModelStatus.OPTIMAL


def run_lp_solve_mps(problem):
    LP_SOLVER_MPS_SOLVER.solve(problem.model, directory=DIRECTORY, delete=DELETE)

    assert problem.model.get_objective().get_value() == OBJECTIVE
    assert all(abs(var.get_value() - sol) < TOLERANCE for var, sol in zip(problem.vars, SOLUTION))
    assert problem.model.get_status() == ModelStatus.OPTIMAL


def run_min_problem():
    problem = setup()
    run_cbc_lp(problem)

    problem.clear()
    run_cbc_mps(problem)

    problem.clear()
    run_cplex_lp(problem)

    problem.clear()
    run_cplex_mps(problem)

    problem.clear()
    run_glpk_lp(problem)

    problem.clear()
    run_glpk_mps(problem)

    problem.clear()
    run_lp_solve_lp(problem)

    problem.clear()
    run_lp_solve_mps(problem)


if __name__ == "__main__":
    run_min_problem()
