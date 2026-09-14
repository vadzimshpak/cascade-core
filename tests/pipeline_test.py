from dotenv import load_dotenv
import unittest

from cascade.program import Program
from cascade.pipeline import Pipeline
from cascade.operator import Execute, Store, Param, JumpOnSuccess
from cascade.stack import Stack

from cascade.commands import *


class TestPipeline1(Pipeline):
    def __init__(self):
        super().__init__()

        self.pipeline = [
            LogCommand(logging.DEBUG, "Pipeline1") >> JumpOnSuccess("test_1"),
            LogCommand(logging.DEBUG, "Pipeline1-1"),

            Label("test_1"),

            LogCommand(logging.DEBUG, "Pipeline2"),

            SetStackCommand("Test0") >> Store("result"),
        ]

class PipelineTest(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.stack = Stack()

    def tearDown(self):
        pass

    def test_basic_pipeline(self):
        result = TestPipeline1() >> Store("res") >> Execute(self.stack)
        if isinstance(result, Exception):
            raise result