import time
from typing import List

class SearchEngine:
    def __init__(self, file_path: str, reread_on_query: bool):
        self.file_path = file_path
        self.reread_on_query = reread_on_query
        self.lines = self.read_file()
        self.last_execution_time = 0

    def read_file(self) -> List[str]:
        with open(self.file_path, "r") as f:
            lines = f.readlines()
        return lines

    def search_string(self, string: str) -> bool:
        start_time = time.time()
        if self.reread_on_query:
            self.lines = self.read_file()
        result = any(string == line.strip() for line in self.lines)
        self.last_execution_time = time.time() - start_time
        return result