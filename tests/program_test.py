from dotenv import load_dotenv
import unittest

from src.program import Program
from src.pipeline import Pipeline
from src.operator import Execute, JumpOnRaise, Store, Param
from src.stack import Stack

from commands import *


class TestPipeline1(Pipeline):
    def __init__(self):
        super().__init__()

        self.pipeline = [
            LogCommand(logging.DEBUG, "Pipeline1"),
            LogCommand(logging.DEBUG, "Pipeline1-1"),

            SetStackCommand("Test0") >> Store("result"),
        ]

class TestPipeline2(Pipeline):
    def __init__(self):
        super().__init__()

    def body(self):
        self.pipeline = [
            DebugStackCommand(),
            LogCommand(logging.DEBUG, "test_1"),
            Param(self._vars[0]) >> Param("test_param") >> DynamicLogCommand(logging.DEBUG),

            SetStackCommand("Test1") >> Store("result")
        ]

        return super().body()

class TestProgram(Program):
    def __init__(self):
        super().__init__()

        self.pipeline = [
            TestPipeline1() >> Store("test_1"),
            Param("test_1") >> TestPipeline2(),
            SetStackCommand("Test2") >> Store("result")
        ]


class ProgramTests(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.stack = Stack()

    def tearDown(self):
        pass

    def test_basic_program(self):
        result = TestProgram() >> Store("res") >> Execute(self.stack)
        if isinstance(result, Exception):
            raise result
        
        print("STACK", self.stack)
        assert self.stack.top()['res'] == "Test2"

