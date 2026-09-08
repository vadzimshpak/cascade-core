from .stack import Stack

class Operator:
    pass

class Execute(Operator):
    def __init__(self, stack: Stack):
        self.stack = stack

class Store(Operator):
    def __init__(self, var_name):
        self.var_name = var_name

class Param(Operator):
    def __init__(self, value, accumulated=None):
        self.values = accumulated if accumulated is not None else []
        self.values.append(value)

    def __rshift__(self, subject):
        if isinstance(subject, Param):
            return Param(subject.values[0], accumulated=self.values)
        
        subject._vars = self.values
        return subject

class RaiseSkip(Operator):
    def __init__(self):
        pass

class RaiseOnSuccess(Operator):
    def __init__(self):
        super().__init__()

class JumpOnRaise(Operator):
    def __init__(self, command_index: int):
        super().__init__()
        self.command_index = command_index

class JumpOnSuccess(Operator):
    def __init__(self, command_index: int):
        super().__init__()
        self.command_index = command_index