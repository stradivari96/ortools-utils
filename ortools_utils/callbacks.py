import time
from threading import Timer
from ortools.sat.python import cp_model


class ObjectiveEarlyStopping(cp_model.CpSolverSolutionCallback):
    """Early Stopping based on Objective improvement"""

    def __init__(self, timer_limit: int, print_objective=False, max_time=None):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._timer_limit = timer_limit
        self._print_objective = print_objective
        self._timer = None  # type: Timer
        self._max_time = max_time
        self._end_time = time.time() + max_time if max_time else None

    def on_solution_callback(self):
        if self._print_objective:
            print(self.ObjectiveValue())
        self.cancel()
        if self._end_time and time.time() >= self._end_time:
            print(f'Time limit reached, obj: {self.ObjectiveValue()}')
            self.StopSearch()
        else:
            self._timer = Timer(self._timer_limit, self.stop)
            self._timer.start()

    def stop(self):
        print(
            'Objective {} not changed in {} seconds, stopping solver...'.format(
                int(self.ObjectiveValue()), self._timer_limit
            )
        )
        self.StopSearch()

    def cancel(self):
        """Cancel the timer if active"""
        if self._timer:
            self._timer.cancel()

    def reset_end_time(self):
        if self._end_time:
            self._end_time = time.time() + self._max_time
