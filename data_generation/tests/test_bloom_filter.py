import sys
sys.path.append('../')

from data_generation.ust import BloomFilter, DiskBloomFilter
import pytest
import string
import random


def test_false_positive():
    b = BloomFilter(1, 2)  # always return a false positive
    b.add('yo')
    b.add('qwop')
    assert 'yo' in b
    assert 'qwop' in b
    assert 'ninja' in b  # always return true even though it isn't in b


def test_contains():
    b = BloomFilter(.1, 5)
    inputs = ['hi', 'there', 'yo', 'ninja', 'time']
    for input in inputs:
        b.add(input)
    for input in inputs:
        assert input in b
    assert not 'ultimatum' in b


def gen(N):
    return ''.join(random.choices(string.ascii_uppercase, k=N))


def compare_prob(size):
    b = BloomFilter(.5, size)
    N = 8
    for i in range(size):
        word = gen(N)
        b.add(word)
        assert word in b  # things that were definitely added are positive.

    # items not in the Bloom should occasionally be false positive.
    # report that it contains an item that it does not
    test_size = 500000
    found = 0
    for i in range(test_size):
        word = gen(N)
        found += word in b
    # fraction of false positives should be around 0.5
    assert found / test_size == pytest.approx(0.5, abs=.1)


def test_larger_bloom():
    compare_prob(1000)


def test_low_prob():
    size = 1000
    b = BloomFilter(.1, size)
    N = 8
    for i in range(size):
        word = gen(N)
        b.add(word)
        assert word in b  # things that were definitely added are positive.

    # items not in the Bloom should occasionally be false positive.
    # report that it contains an item that it does not
    test_size = 500000
    found = 0
    for i in range(test_size):
        word = gen(N)
        found += 1 if word in b else 0
    # fraction of false positives should be around 0.5
    assert found / test_size == pytest.approx(0.1, abs=.05)


def test_disk_false_positive():
    # with prob 1 it always returns positive.
    b = DiskBloomFilter(1, 2, './', 'disk_bloom.dat')
    b.add('yo')
    b.add('qwop')
    assert 'yo' in b
    assert 'qwop' in b
    assert 'ninja' in b  # always return true even though it isn't in b
    assert 'b' in b
    assert 'bob' in b
    assert 'bobcat' in b


def test_disk_contains():
    b = DiskBloomFilter(.01, 5, './', 'disk_bloom.dat')
    inputs = ['hi', 'there', 'yo', 'ninja', 'time']
    for input in inputs:
        b.add(input)
    for input in inputs:
        assert input in b
    assert not 'ultimatum' in b
    assert not 'tootoo' in b
    assert not 'floofloo' in b


def test_low_prob():
    size = 1000
    b = DiskBloomFilter(.1, size, './', 'disk_bloom.dat')
    N = 8
    for i in range(size):
        word = gen(N)
        b.add(word)
        assert word in b  # things that were definitely added are positive.

    # items not in the Bloom should occasionally be false positive.
    # report that it contains an item that it does not
    test_size = 500000
    found = 0
    for i in range(test_size):
        word = gen(N)
        found += 1 if word in b else 0
    # fraction of false positives should be around 0.5
    assert found / test_size == pytest.approx(0.1, abs=.05)
