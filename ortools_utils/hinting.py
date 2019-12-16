from ortools.sat.python import cp_model


def hint_solution(model: cp_model.CpModel, solver: cp_model.CpSolver) -> None:
    """Hint all the variables of a model with its solution."""
    model.Proto().solution_hint.Clear()
    variables = range(len(model.Proto().variables))
    model.Proto().solution_hint.vars.extend(variables)
    model.Proto().solution_hint.values.extend(solver.ResponseProto().solution)


def check_hint(model: cp_model.CpModel) -> bool:
    """Check the hinted solution is valid"""
    # No hint
    if not model.Proto().solution_hint.vars:
        return True
    # Clone model
    tmp_model = cp_model.CpModel()
    tmp_model.Proto().CopyFrom(model.Proto())

    solver = cp_model.CpSolver()
    variables = tmp_model.Proto().solution_hint.vars
    values = tmp_model.Proto().solution_hint.values
    for i, var in enumerate(variables):
        var = tmp_model.Proto().variables[var]
        value = values[i]
        lb, ub = var.domain
        if not (lb <= value <= ub):
            # outside the domain
            return False
        var.ClearField("domain")
        var.domain.extend([value, value])

    # hopefully presolved
    status = solver.Solve(tmp_model)
    return status in [cp_model.FEASIBLE, cp_model.OPTIMAL]
