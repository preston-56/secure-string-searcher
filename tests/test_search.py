from search.search import SearchEngine

def test_search_string_exists():
    search_engine = SearchEngine('/home/code/string-searcher/data/200k.txt', False)
    with open('/home/code/string-searcher/data/200k.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            assert search_engine.search_string(line.strip())

def test_search_string_not_found():
    search_engine = SearchEngine('/home/code/string-searcher/data/200k.txt', False)
    assert not search_engine.search_string('non-existent string')