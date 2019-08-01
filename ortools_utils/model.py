import logging
from ortools.sat.python import cp_model


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
