#!/usr/bin/env python
from shutil import rmtree

from mosi.common import ModelStatus
from mosi.lp import Model, FloatVariable

# noinspection PyPackageRequirements,PyUnresolvedReferences
from init import (
    CBC_LP_SOLVER, CBC_MPS_SOLVER, CPLEX_LP_SOLVER, CPLEX_MPS_SOLVER,
    GLPK_LP_SOLVER, GLPK_MPS_SOLVER, LP_SOLVER_LP_SOLVER, LP_SOLVER_MPS_SOLVER, Problem
)

DELETE = True
DIRECTORY = "../../../volume/results/lp"
OBJECTIVE = 140
SOLUTION = [-40.0, -110.0, 0.0]
TOLERANCE = 10 ** -8


# noinspection PyStatementEffect
def setup():
    rmtree(DIRECTORY, True)

    model = Model(auto=True)

    x = {
        1: FloatVariable(model, min=-40),
        2: FloatVariable(model, min=-float("inf")),
        3: FloatVariable(model)
    }

    model.max(
        2 * x[1] - 2 * x[2] + x[3]
    )

    2 * x[1] - x[2] + x[3] <= 80
    3 * x[1] - 2 * x[2] + 2 * x[3] <= 100
    x[1] + x[2] + x[3] <= 40

    return Problem(model, list(x.values()))


def run_cbc_lp(problem):
    CBC_LP_SOLVER.solve(problem.model, directory=DIRECTORY, delete=DELETE)

    assert problem.model.get_status() == ModelStatus.OPTIMAL
    assert all(abs(var.get_value() - sol) < TOLERANCE for var, sol in zip(problem.vars, SOLUTION))
    assert [var.get_value() for var in problem.vars] == SOLUTION


def run_cbc_mps(problem):
    CBC_MPS_SOLVER.solve(problem.model, directory=DIRECTORY, delete=DELETE)

    assert problem.model.get_status() == ModelStatus.OPTIMAL
    assert all(abs(var.get_value() - sol) < TOLERANCE for var, sol in zip(problem.vars, SOLUTION))
    assert [var.get_value() for var in problem.vars] == SOLUTION


def run_cplex_lp(problem):
    CPLEX_LP_SOLVER.solve(problem.model, directory=DIRECTORY, delete=DELETE)

    assert problem.model.get_status() == ModelStatus.OPTIMAL
    assert all(abs(var.get_value() - sol) < TOLERANCE for var, sol in zip(problem.vars, SOLUTION))
    assert [var.get_value() for var in problem.vars], SOLUTION


def run_cplex_mps(problem):
    CPLEX_MPS_SOLVER.solve(problem.model, directory=DIRECTORY, delete=DELETE)

    assert problem.model.get_status() == ModelStatus.OPTIMAL
    assert all(abs(var.get_value() - sol) < TOLERANCE for var, sol in zip(problem.vars, SOLUTION))
    assert [var.get_value() for var in problem.vars] == SOLUTION


def run_glpk_lp(problem):
    GLPK_LP_SOLVER.solve(problem.model, directory=DIRECTORY, delete=DELETE)

    assert problem.model.get_status() == ModelStatus.OPTIMAL
    assert all(abs(var.get_value() - sol) < TOLERANCE for var, sol in zip(problem.vars, SOLUTION))
    assert [var.get_value() for var in problem.vars] == SOLUTION


def run_glpk_mps(problem):
    GLPK_MPS_SOLVER.solve(problem.model, directory=DIRECTORY, delete=DELETE)

    assert problem.model.get_status() == ModelStatus.OPTIMAL
    assert all(abs(var.get_value() - sol) < TOLERANCE for var, sol in zip(problem.vars, SOLUTION))
    assert [var.get_value() for var in problem.vars], SOLUTION


def run_lp_solve_lp(problem):
    LP_SOLVER_LP_SOLVER.solve(problem.model, directory=DIRECTORY, delete=DELETE)

    assert problem.model.get_status() == ModelStatus.OPTIMAL
    assert all(abs(var.get_value() - sol) < TOLERANCE for var, sol in zip(problem.vars, SOLUTION))
    assert [var.get_value() for var in problem.vars], SOLUTION


def run_lp_solve_mps(problem):
    LP_SOLVER_MPS_SOLVER.solve(problem.model, directory=DIRECTORY, delete=DELETE)

    assert problem.model.get_status() == ModelStatus.OPTIMAL
    assert all(abs(var.get_value() - sol) < TOLERANCE for var, sol in zip(problem.vars, SOLUTION))
    assert [var.get_value() for var in problem.vars] == SOLUTION


def run_free_problem():
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

    print("done :)")

if __name__ == "__main__":
    run_free_problem()
