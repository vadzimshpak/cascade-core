import base64

class Resource:
    def __init__(self, path: str):
        self.path = path

    def openAsBase64(self):
        with open(self.path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
