import logging
import datetime as dt
from typing import Optional
from ortools.sat.python import cp_model

from .hinting import hint_solution


def export_proto(model: cp_model.CpModel, filepath):
    with open(filepath, "w") as f:
        f.write(str(model.Proto()))


def log_num_vars(model: cp_model.CpModel, step_name: str, level='debug'):
    level = level.lower().strip()
    level_options = ['debug', 'info', 'warning', 'error', 'critical']
    if level not in level_options:
        raise Exception(f'Unknown level "{level}", {level_options}')
    getattr(logging, level)(
        f'"{step_name}": '
        f'Vars: {len(model.Proto().variables)}, '
        f'Constr: {len(model.Proto().constraints)}'
    )


def solve_intermediate_objective(
    model: cp_model.CpModel,
    solver: cp_model.CpSolver,
    objective,
    hint=True,
    objective_type='min',
    callback: Optional[cp_model.CpSolverSolutionCallback] = None,
    alias=None,
    max_time=None,
    logger=logging
):

    if max_time:
        solver.parameters.max_time_in_seconds = max_time

    if objective_type.lower().startswith('min'):
        model.Minimize(objective)
        objective_type = 'min'
    elif objective_type.lower().startswith('max'):
        model.Maximize(objective)
        objective_type = 'max'
    else:
        raise Exception(f'Can not "{objective_type}" objective')

    t0 = dt.datetime.now()
    if callback:
        status = solver.SolveWithSolutionCallback(model, callback)
    else:
        status = solver.Solve(model)
    duration = (dt.datetime.now() - t0).total_seconds()

    if status == cp_model.INFEASIBLE:
        logger.warning(f'INFEASIBLE solving {alias or objective}')
        return None, status
    elif status == cp_model.UNKNOWN:
        logger.warning(f'Time limit reached {alias or objective}')
        return None, status
    result = round(solver.ObjectiveValue())

    if hint:
        hint_solution(model, solver)
    if status == cp_model.OPTIMAL:
        logger.debug(
            f'{alias or objective} == {result}, Seconds: {duration:.2f}'
        )
        model.Add(objective == result)
    elif objective_type == 'min':
        logger.debug(
            f'{alias or objective} <= {result}, Seconds: {duration:.2f}'
        )
        model.Add(objective <= result)
    elif objective_type == 'max':
        logger.debug(
            f'{alias or objective} >= {result}, Seconds: {duration:.2f}'
        )
        model.Add(objective >= result)
    return result, status
