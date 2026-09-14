import unittest

from cascade.commands import *
from cascade.operator import Execute
from cascade.stack import Stack


class CommandTests(unittest.TestCase):
    def setUp(self):
        self.stack = Stack()

    def tearDown(self):
        pass

    def test_log_command(self):
        LogCommand(logging.INFO, "test") >> Execute(self.stack)

    def test_dynamic_log_command(self):
        LogExceptionCommand(Exception("test")) >> Execute(self.stack)
