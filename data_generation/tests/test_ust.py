import sys
sys.path.append('../')

from data_generation.ust import SetUST


def test_set_ust():
    ust = SetUST()
    ust.add('"hi.com"')
    ust.add('"yolo.com"')
    ust.add('"ninja.net"')

    assert '"hi.com"' in ust
    assert not 'hi.com' in ust
    assert '"yolo.com"' in ust
    assert '"ninja.net"' in ust
    assert ust.contains('"hi.com"')
    assert not ust.contains('poop')
    assert not ust.contains('')
    ust.add('')
    assert '' in ust
