import logging
import sys
import os
import requests
import mss
import mss.tools
import io


class ConsoleHandler(logging.StreamHandler):
    def __init__(self, log_level: str, stream):
        super().__init__(stream)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        self.setFormatter(formatter)
        self.setLevel(log_level)

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


def get_logger(name: str):
    log_level = os.getenv("LOG_LEVEL", "DEBUG")
    tg_token = os.getenv("TG_BOT_TOKEN", None)
    tg_chats = os.getenv("TG_BOT_CHATS", None)
    tg_log_level = os.getenv("TG_LOG_LEVEL", "INFO")
    tg_image_on_error = os.getenv("TG_IMAGE_ON_ERROR", 0) == "1"

    logger = logging.getLogger(f"genshin_game.[{name}]")
    logger.setLevel(logging.DEBUG)

    logger.addHandler(ConsoleHandler(log_level, sys.stdout))
    logger.addHandler(CustomFileHandler("log.txt"))

    if tg_token and tg_chats:
        logger.addHandler(TGHandler(tg_token, tg_chats, tg_log_level, tg_image_on_error))

    return logger