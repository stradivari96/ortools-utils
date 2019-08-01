from ortools.sat.python import cp_model


def hint_solution(model: cp_model.CpModel, solver: cp_model.CpSolver) -> None:
    """Hint all the variables of a model with its solution."""
    model.Proto().solution_hint.Clear()
    for i in range(len(model.Proto().variables)):
        model.Proto().solution_hint.vars.append(i)
        model.Proto().solution_hint.values.append(
            solver.ResponseProto().solution[i]
        )


def hint_variable(model, var: cp_model.IntVar, value: int):
    """Hint a variable, will be replaced by model.AddHint in ortools >= 7.3"""
    model.Proto().solution_hint.vars.append(var.Index())
    model.Proto().solution_hint.values.append(value)
