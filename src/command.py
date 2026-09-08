import time
import random
from typing import TYPE_CHECKING, Self

from .logger import get_logger
from .stack import Stack


if TYPE_CHECKING:
    from .operator import Operator


logger = get_logger(__name__)
random.seed(time.time())

class Command:
    def __init__(self):
        self._store_var = None
        self._stack: Stack = None
        self._skip_on_raise = False
        self._jump_on_raise = None
        self._raise_on_success = False
        self._jump_on_success = None
        self._vars = []

    def execute(self, stack: Stack):
        logger.debug(f"Execute subject: {type(self).__name__}")

        self._stack = stack
        result = self.body()

        if type(result) is str:
            logger.debug(f"Got {result if len(result) < 100 else result[:100] + "..."} from {type(self).__name__}")
        else:
            logger.debug(f"Got {result} from {type(self).__name__}")

        if self._store_var:
            stack.update(self._store_var, result)

        return result

    def body(self):
        raise Exception("This subject doesn't have body!")

    def get_param_value(self, number: int):
        return self._stack.top_value(self._vars[number])

    def __rshift__(self, command: Operator) -> Self | object | Exception:
        from .operator import Execute, Store, RaiseSkip, JumpOnRaise, JumpOnSuccess, RaiseOnSuccess

        if type(command) == Execute:
            try:
                return self.execute(command.stack)
            except Exception as e:
                return e

        elif type(command) == Store:
            self._store_var = command.var_name

        elif type(command) == RaiseSkip:
            self._skip_on_raise = True

        elif type(command) == RaiseOnSuccess:
            self._raise_on_success = True

        elif type(command) == JumpOnRaise:
            self._jump_on_raise = command.command_index

        elif type(command) == JumpOnSuccess:
            self._jump_on_success = command.command_index

        return self