from threading import Timer
from ortools.sat.python import cp_model


class ObjectiveEarlyStopping(cp_model.CpSolverSolutionCallback):
    """Early Stopping based on Objective improvement"""

    def __init__(self, time_limit: int, print_objective=False):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._time_limit = time_limit
        self._print_objective = print_objective
        self._timer = None

    def on_solution_callback(self):
        if self._print_objective:
            print(self.ObjectiveValue())
        if not self._timer:
            self._timer = Timer(self._time_limit, self.stop)
            self._timer.start()
        else:
            self._timer.cancel()
            self._timer = Timer(self._time_limit, self.stop)
            self._timer.start()

    def stop(self):
        print(
            'Objective {} not changed in {} seconds, stopping solver...'.format(
                int(self.ObjectiveValue()), self._time_limit
            )
        )
        self.StopSearch()
