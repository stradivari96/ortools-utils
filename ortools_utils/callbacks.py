import time
from threading import Timer
from ortools.sat.python import cp_model


class ObjectiveEarlyStopping(cp_model.CpSolverSolutionCallback):
    """Early Stopping based on Objective improvement"""

    def __init__(
        self,
        timer_limit: int,
        print_objective=False,
        max_time=None,
        logger=None
    ):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._logger = logger
        self._timer_limit = timer_limit
        self._print_objective = print_objective
        self._timer = None  # type: Timer
        self._max_time = max_time
        self._end_time = time.time() + max_time if max_time else None

    def on_solution_callback(self):
        if self._print_objective:
            self._print_or_log(self.ObjectiveValue())
        self.cancel()
        if self._end_time and time.time() >= self._end_time:
            self._print_or_log(
                f'Time limit reached, obj: {self.ObjectiveValue()}'
            )
            self.StopSearch()
        else:
            if not self._timer:
                self._print_or_log(
                    f'First objective found: {self.ObjectiveValue()}'
                )
            self._timer = Timer(self._timer_limit, self.stop)
            self._timer.start()

    def stop(self):
        self._print_or_log(
            f'Objective {self.ObjectiveValue()} not changed in {self._timer_limit} seconds'
        )
        self.StopSearch()

    def cancel(self):
        """Cancel the timer if active"""
        if self._timer:
            self._timer.cancel()

    def reset_end_time(self):
        if self._end_time:
            self._end_time = time.time() + self._max_time

    def _print_or_log(self, msg):
        if self._logger:
            self._logger.debug(msg)
        else:
            print(msg)
