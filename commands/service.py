import time
import random
import logging

if __package__ and "." in __package__:
    from ..src.command import Command
    from ..src.logger import get_logger
else:
    from src.command import Command
    from src.logger import get_logger


logger = get_logger(__name__)
random.seed(time.time())


class SleepCommand(Command):
    """
    Sleep n seconds
    """
    
    def __init__(self, secs: int):
        super().__init__()
        self.secs = secs

    def body(self):
        time.sleep(self.secs)

class SleepRandomRangeCommand(Command):
    """
    Sleep a random number of seconds within a range
    """

    def __init__(self, secs_from: int, secs_to: int):
        super().__init__()
        self.secs_from = secs_from
        self.secs_to = secs_to

    def body(self):
        time.sleep(random.randrange(self.secs_from, self.secs_to))

class LogCommand(Command):
    """
    Log a message at a specified level
    """

    def __init__(self, level: int, message: str):
        super().__init__()
        self.level = level
        self.message = message

    def body(self):
        logger.log(self.level, self.message)

class LogExceptionCommand(Command):
    """
    Log an exception at the ERROR level
    """

    def __init__(self, exception: object):
        super().__init__()
        self.exception = exception

    def body(self):
        logger.log(logging.ERROR, self.exception)

class DynamicLogCommand(Command):
    """
    Log a dynamic message at a specified level
    """

    def __init__(self, level: int):
        super().__init__()
        self.level = level

    def body(self):
        message = self.get_param_value(0)
        logger.log(self.level, message)

class SetStackCommand(Command):
    """
    Set the stack to a specified value, need to use with Store(<var>) operator!
    """

    def __init__(self, value):
        super().__init__()
        self.value = value

    def body(self):
        return self.value

class DebugStackCommand(Command):
    """
    Debug the current stack
    """

    def __init__(self):
        super().__init__()

    def body(self):
        logger.debug("Stack: " + repr(self._stack))
        
class RaiseCommand(Command):
    """
    Raise an exception
    """

    def __init__(self):
        super().__init__()

    def body(self):
        raise Exception("Test raise")