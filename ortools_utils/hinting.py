from ortools.sat.python import cp_model


def hint_solution(model: cp_model.CpModel, solver: cp_model.CpSolver) -> None:
    """Hint all the variables of a model with its solution."""
    model.Proto().solution_hint.Clear()
    variables = range(len(model.Proto().variables))
    model.Proto().solution_hint.vars.extend(variables)
    model.Proto().solution_hint.values.extend(solver.ResponseProto().solution)
