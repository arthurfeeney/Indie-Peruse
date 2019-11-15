import sys
sys.path.append('../')

from frontier import *


def test_fifo_frontier():
    f = FIFOFrontier()
    assert (f.view_frontier() == [])
    f.add('hi')
    f.add('yo')
    f.add('swag')
    assert not f.empty()
    assert (f.view_frontier() == ['hi', 'yo', 'swag'])
    assert (f.get() == 'hi')
    assert (f.view_frontier() == ['yo', 'swag'])
    assert (f.get() == 'yo')
    assert (f.view_frontier() == ['swag'])
    assert (f.get() == 'swag')
    assert (f.view_frontier() == [])
    assert f.empty()


def test_k_oldest():
    # test for DomainPriorityFrontier.__k_oldest
    f = memory_domain_priority_frontier()

    urls = [
        'https://hi.com/two', 'http://there.com/xyz', 'https://ninja.com/abc'
    ]
    for url in urls:
        f.add(url)

    assert f.priority_functor.k_oldest(1) == ['https://hi.com']
    assert f.priority_functor.k_oldest(2) == [
        'https://hi.com', 'http://there.com'
    ]


def test_dp_frontier_limit():
    f = memory_domain_priority_frontier(limit=2)
    urls = [
        'https://hi.com/two', 'http://there.com/xyz', 'https://ninja.com/abc'
    ]
    for url in urls:
        f.add(url)
    assert list(f.priority_functor.last_pulled.keys()) == ['https://ninja.com']


def simple_frontier_size(f):
    assert f.size() == 0
    assert f.empty()
    f.add('hey')
    f.add('there')
    assert f.size() == 2
    f.add('hi')
    assert f.size() == 3
    assert not f.empty()
    f.get()
    assert f.size() == 2
    f.get()
    f.get()
    assert f.size() == 0
    assert f.empty()


def test_frontier_size():
    simple_frontier_size(FIFOFrontier())
    simple_frontier_size(memory_domain_priority_frontier())
    simple_frontier_size(memory_seen_priority_frontier())
