import json
import os
import tempfile
from threading import Lock


class JsonRepository:
    def __init__(self, file_path):
        self.file_path = file_path
        self.lock = Lock()

    def read(self):
        with self.lock:
            if not os.path.exists(self.file_path):
                return {
                    "vehicles": [],
                    "brands": []
                }

            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)

    def write(self, data):
        with self.lock:
            directory = os.path.dirname(self.file_path)

            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=directory,
                delete=False
            ) as temp_file:

                json.dump(
                    data,
                    temp_file,
                    ensure_ascii=False,
                    indent=2
                )

                temp_path = temp_file.name

            os.replace(temp_path, self.file_path)