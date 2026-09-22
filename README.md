# Cascade Core

<p align="center">
  <img src="./media/logo.png" width="250">
</p>

<div align="center">

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/downloads/)
[![Version 0.1.41](https://img.shields.io/badge/Version-0.1.41-green)](https://github.com/vadzimshpak/cascade-core/releases)
[![Tests](https://img.shields.io/github/actions/workflow/status/vadzimshpak/cascade-core/main.yml?branch=main&label=Tests)](https://github.com/vadzimshpak/cascade-core/actions)

</div>

Arch:
- Command - smallest part
- Pipeline - mix of commands
- Program - mix of commands and pipelines
- [Next level...]
- [Next level...]

Philosophy:

    - Each well-tested and documented command is part of the sucessfull pipeline.
        - Each well-tested and documented pipeline is part of the sucessfull program.
            - Each well-tested and documented program is part of the sucessfull cascade.
                - Each well-tested and documented cascade is part of the sucessfull business.

Add submodule to project:
`git submodule add https://github.com/vadzimshpak/cascade-core cascade`

---

### Example of a custom command:

```python
import logging

from cascade.command import Command

logger = logging.getLogger("cascade")


class DynamicLogCommand(Command):
    """
    Log a dynamic message at a specified level.
    Reads the value from the execution stack and formats it.
    """

    def __init__(self, level: int, format: str = "%s"):
        super().__init__()
        self.level = level
        self.format = format

    def body(self):
        message = self.get_param_value(0)
        logger.log(self.level, self.format % message)
```

### Example of a custom pipeline:

```python
import logging

from cascade.pipeline import Pipeline
from cascade.operator import Store, Param
from cascade.commands import *


class DynamicLogPipeline(Pipeline):
    """
    Pipeline with a couple of commands.
    """

    def __init__(self):
        super().__init__()

        self.pipeline = [
            SetStackCommand("Hello world!") >> Store("test_0"),
            Param("test_0") >> DynamicLogCommand(logging.INFO, "My string: %s"),
            LogCommand(logging.INFO, "Pipeline finished"),
        ]
```

### Example of a custom program:

```python
import logging

from cascade.program import Program
from cascade.commands import *


class DynamicLogProgram(Program):
    """
    Program with a couple of subjects.
    """

    def __init__(self):
        super().__init__()

        self.pipeline = [
            DynamicLogPipeline(),
            LogCommand(logging.INFO, "Hello World!"),
        ]
```

### Running each part of the flow:

```python
import logging

from cascade.operator import Execute
from cascade.commands import *
from cascade.logger import init_logger
from cascade import Stack

init_logger()
stack = Stack()

# Run command
LogCommand(logging.INFO, "Hello world!") >> Execute(stack)

# Run pipeline
DynamicLogPipeline() >> Execute(stack)

# Run program
DynamicLogProgram() >> Execute(stack)
```

---

### Creating your own level of cascade:

```python
from cascade.program import Program
from cascade.operator import Execute
from cascade.logger import init_logger
from cascade import Stack

init_logger()
stack = Stack()


class Cascade(Program):
    def __init__(self):
        super().__init__()


class DynamicLogCascade(Cascade):
    def __init__(self):
        super().__init__()

        self.pipeline = [
            DynamicLogProgram()
        ]


DynamicLogCascade() >> Execute(stack)
```

---

### Adding handlers to logging
```python
import logging
import requests
import mss
import mss.tools
import io
import os



def init_cascade_logger():
    from cascade.logger import init_logger
    init_logger()

    logger = logging.getLogger("cascade")

    tg_token = os.getenv("TG_BOT_TOKEN", None)
    tg_chats = os.getenv("TG_BOT_CHATS", None)
    tg_log_level = os.getenv("TG_LOG_LEVEL", "INFO")
    tg_image_on_error = os.getenv("TG_IMAGE_ON_ERROR", 0) == "1"

    logger.addHandler(CustomFileHandler("log.txt", encoding="utf8"))

    if tg_token and tg_chats:
        logger.addHandler(TGHandler(tg_token, tg_chats, tg_log_level, tg_image_on_error))


class TGHandler(logging.Handler):
    def __init__(self, token: str, chats: str, level: str, image_on_error: bool):
        super().__init__()
        self.chats = chats.split(',')
        self.image_on_error = image_on_error
        self.url = f"https://api.telegram.org/bot{token}/sendMessage"
        self.image_url = f"https://api.telegram.org/bot{token}/sendPhoto"

        formatter = logging.Formatter("%(levelname)s - %(message)s")
        self.setFormatter(formatter)
        self.setLevel(level)

    def emit(self, record):
        log_entry = self.format(record)

        for chat in self.chats:
            payload = {
                "chat_id": chat,
                "text": log_entry
            }

            requests.post(self.url, json=payload)
    
        if not self.image_on_error:
            return

        if record.levelno < logging.ERROR:
            return

        with mss.mss() as sct:
            monitor = sct.monitors[1]
            sct_img = sct.grab(monitor)
            png_bytes = mss.tools.to_png(sct_img.rgb, sct_img.size)

        image_file = io.BytesIO(png_bytes)
        image_file.name = 'screenshot.png'

        for chat in self.chats:
            payload = {'chat_id': chat}
            files = {'photo': image_file}

            requests.post(self.image_url, data=payload, files=files)

class CustomFileHandler(logging.FileHandler):
    def __init__(self, filename, mode = "a", encoding = None, delay = False, errors = None):
        super().__init__(filename, mode, encoding, delay, errors)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        self.setFormatter(formatter)
        self.setLevel(logging.DEBUG)
```

### Usage:

```python
import logging
import winsound

from cascade.command import Command
from cascade.operator import Execute
from cascade.stack import Stack
from cascade.logger import init_logger


logger = logging.getLogger(f"cascade.{__name__}")


class BeepCommand(Command):
    """Beep command."""

    def __init__(self, frequency: int = 1000, duration: int = 500):
        super().__init__()
        self.frequency = frequency
        self.duration = duration

    def body(self):
        logger.debug("DEBUG STRING")
        winsound.Beep(self.frequency, self.duration)


init_logger()
stack = Stack()
BeepCommand() >> Execute(stack)
```