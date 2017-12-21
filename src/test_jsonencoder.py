from jsonencoder import jsonencoder
import json

def test_encode_single_thing(benchmark):
    result = benchmark(encode_single_thing)

def test_dont_encode_single_thing(benchmark):
    result = benchmark(dont_encode_single_thing)


# pip install pytest-benchmark
def encode_single_thing():
    """
    Function that needs some serious benchmarking.
    """
    a = {
        "time": 12398123,
        "ab:cd:ef": -12,
        "cd:df": -20,
        "user": "zack"
    }
    c = jsonencoder()
    return c.encode(a)

# pip install pytest-benchmark
def dont_encode_single_thing():
    """
    Function that needs some serious benchmarking.
    """
    a = {
        "time": 12398123,
        "ab:cd:ef": -12,
        "cd:df": -20,
        "user": "zack"
    }
    return json.dumps(a)


def test_encode():
    a = {
        "time": 12398123,
        "ab:cd:ef": -12,
        "cd:df": -20,
        "user": "zack"
    }

    b = {
        "time": 3333398123,
        "ab:cd:ef": -22,
        "cd:df": -10,
        "user": "zack"
    }

    c = jsonencoder()
    a_enc = c.encode(a)

    c_string = c.dumps()
    d = jsonencoder()
    d.loads(c_string)
    b_enc = d.encode(b)

    assert 4 == d.compressor['num']
    assert d.decode(b_enc) == b
    assert d.decode(a_enc) == a
    assert c.decode(b_enc) is not b
