import base64
import cv2

class Resource:
    def __init__(self, path: str):
        self.path = path

    def openAsMatLike(self):
        template = cv2.imread(self.path)
        return template

    def openAsBase64(self):
        with open(self.path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
