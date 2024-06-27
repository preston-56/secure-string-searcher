from server.utils import read_file
from search.search import SearchEngine
from server.server import StringSearchServer

class TestUtils:
    def test_read_file(self):
        lines = read_file('/home/code/string-searcher/data/200k.txt')
        assert len(lines) == 271100