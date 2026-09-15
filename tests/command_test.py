import unittest

from cascade.commands import *
from cascade.operator import Execute
from cascade.stack import Stack
from cascade.logger import init_logger


class CommandTests(unittest.TestCase):
    def setUp(self):
        self.stack = Stack()
        init_logger()

    def tearDown(self):
        pass

    def test_log_command(self):
        LogCommand(logging.INFO, "test") >> Execute(self.stack)

    def test_dynamic_log_command(self):
        try:
            raise Exception("test")
        except Exception as e:
            LogExceptionCommand(e) >> Execute(self.stack)
