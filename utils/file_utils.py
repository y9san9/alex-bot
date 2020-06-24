import json
import os
from typing import Callable, Any


class File:
    def __init__(self, filename: str):
        self.filename = filename

    def refresh(self, default_text: str = ""):
        if not os.path.isfile(self.filename):
            self.write(default_text)

    def write(self, text: str):
        with open(self.filename, 'w') as file:
            file.write(text)

    def read(self) -> str:
        with open(self.filename, 'r') as file:
            return file.read()

    def write_object(self, obj):
        self.write(json.dumps(obj))

    def read_object(self, object_hook: Callable[[dict], Any] = lambda x: x):
        return json.loads(self.read(), object_hook=object_hook)
