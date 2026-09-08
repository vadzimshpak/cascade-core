from .command import Command
from .logger import get_logger

logger = get_logger(__name__)

class Pipeline(Command):
    def __init__(self):
        super().__init__()
        self.pipeline = []

    def _process_chain(self, chain: list):
        from .operator import Execute
        self._stack.push({} if not self._stack.top() else self._stack.top().copy())
        self._stack.update("__debug_name", type(self).__name__)

        i = 0
        while i < len(chain):
            subject = chain[i]
            i += 1

            if type(subject) == list:
                self._process_chain(subject)
                continue

            result = subject >> Execute(self._stack)

            if isinstance(result, Exception):
                if subject._jump_on_raise is not None:
                    i = subject._jump_on_raise
                    logger.debug(f"{type(self).__name__} jump to {i} subject")
                    continue

                if subject._skip_on_raise:
                    logger.debug(f"{type(self).__name__} skip pipeline")
                    break
                else:
                    logger.debug(f"{type(self).__name__} raise")
                    raise result

            if subject._raise_on_success:
                logger.debug(f"{type(self).__name__} success raise")
                raise Exception("Success raise")


            if subject._jump_on_success is not None:
                i = subject._jump_on_success
                logger.debug(f"{type(self).__name__} jump to {i} subject")
                continue

        result = self._stack.pop()
        return result.get("result")

    def body(self):
        return self._process_chain(self.pipeline)
