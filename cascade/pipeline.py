from .command import Command
from .logger import get_logger

logger = get_logger(__name__)

class Pipeline(Command):
    def __init__(self):
        super().__init__()
        self.pipeline = []

    def _process_chain(self, chain: list):
        from .operator import Execute
        from .commands import Label

        self._stack.push({} if not self._stack.top() else self._stack.top().copy())
        self._stack.update("__debug_name", type(self).__name__)

        i = 0

        def get_label_index(label_name: str):
            for index, subject in enumerate(chain):
                if isinstance(subject, Label) and subject.label_name == label_name:
                    return index

            raise Exception(f"Label {label_name} not found in pipeline")

        while i < len(chain):
            subject = chain[i]
            i += 1

            if type(subject) == list:
                self._process_chain(subject)
                continue

            result = subject >> Execute(self._stack)

            if isinstance(result, Exception):
                logger.debug(result)
                if subject._jump_on_raise is not None:
                    i = get_label_index(subject._jump_on_raise)
                    logger.debug(f"{type(self).__name__} jump to {i} subject")
                    continue

                if subject._skip_on_raise:
                    logger.debug(f"{type(self).__name__} skip pipeline")
                    break
                else:
                    logger.debug(f"{type(self).__name__} raise")
                    raise result


            if subject._jump_on_success is not None:
                i = get_label_index(subject._jump_on_success)
                logger.debug(f"{type(self).__name__} jump to {i} subject")
                continue

        result = self._stack.pop()
        return result.get("result")

    def body(self):
        return self._process_chain(self.pipeline)