from config.config import read_config

def test_load_config():
    cfg = read_config()
    assert cfg[0] == '0.0.0.0'
    assert cfg[1] == 44445
    assert cfg[2] == '/home/code/string-searcher/data/200k.txt'
    assert cfg[3] is True
    assert cfg[4] is True  # SSL_ENABLED should be True
    assert cfg[5] == 'server.crt'
    assert cfg[6] == 'server.key'