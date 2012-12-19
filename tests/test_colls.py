import pytest
from itertools import count
from collections import Iterator, defaultdict
from whatever import _

from funcy.colls import *


# Utilities
def eq(a, b):
    return type(a) is type(b) and a == b \
       and (a.default_factory == b.default_factory if isinstance(a, defaultdict) else True)

def inc(x):
    return x + 1

def hinc(xs):
    return map(inc, xs)


def test_empty():
    assert eq(empty({'a': 1}), {})
    assert eq(empty(defaultdict(int)), defaultdict(int))
    assert empty(defaultdict(int)).default_factory == defaultdict(int).default_factory

def test_iteritems():
    assert list(iteritems([1,2])) == [1,2]
    assert list(iteritems((1,2))) == [1,2]
    assert list(iteritems({'a': 1})) == [('a', 1)]

def test_join():
    assert pytest.raises(TypeError, join, [])
    assert eq(join(['', 'ab', 'cd']), 'abcd')
    assert eq(join([['a', 'b'], 'c']), list('abc'))
    assert eq(join([('a', 'b'), ('c',)]), tuple('abc'))
    assert eq(join([{'a': 1}, {'b': 2}]), {'a': 1, 'b': 2})
    assert eq(join([{'a': 1}, {'a': 2}]), {'a': 2})
    assert eq(join([{1,2}, {3}]), {1,2,3})

    it1 = (x for x in range(2))
    it2 = (x for x in range(5, 7))
    joined = join([it1, it2])
    assert isinstance(joined, Iterator) and list(joined) == [0,1,5,6]

    dd1 = defaultdict(int, a=1)
    dd2 = defaultdict(int, b=2)
    assert eq(join([dd1, dd2]), defaultdict(int, a=1, b=2))


def test_walk():
    assert eq(walk(inc, [1,2,3]), [2,3,4])
    assert eq(walk(inc, (1,2,3)), (2,3,4))
    assert eq(walk(inc, {1,2,3}), {2,3,4})
    assert eq(walk(hinc, {1:1,2:2,3:3}), {2:2,3:3,4:4})

def test_walk_keys():
    assert walk_keys(str.upper, {'a': 1, 'b':2}) == {'A': 1, 'B': 2}

def test_walk_values():
    assert walk_values(_ * 2, {'a': 1, 'b': 2}) == {'a': 2, 'b': 4}

    dd = defaultdict(int, {'a': 1, 'b': 2})
    walked_dd = walk_values(_ * 2, dd)
    assert walked_dd == {'a': 2, 'b': 4}
    assert walked_dd.default_factory is dd.default_factory

def test_select():
    assert eq(select(_>1, [1,2,3]), [2,3])
    assert eq(select(_>1, (1,2,3)), (2,3))
    assert eq(select(_>1, {1,2,3}), {2,3})
    assert eq(select(_[1]>1, {'a':1,'b':2,'c':3}), {'b':2,'c':3})
    assert select(_[1]>1, defaultdict(int)) == {}

def test_select_keys():
    assert select_keys(_[0] == 'a', {'a':1, 'b':2, 'ab':3}) == {'a': 1, 'ab':3}

def test_select_values():
    assert select_values(_ % 2, {'a': 1, 'b': 2}) == {'a': 1}


def test_is_distinct():
    assert is_distinct('abc')
    assert not is_distinct('aba')


def test_all():
    assert all([1,2,3])
    assert not all([1,2,''])
    assert all(callable, [abs, open, int])
    assert not all(_ < 3, [1,2,5])

def test_any():
    assert any([0, False, 3, ''])
    assert any([0, False, '']) == False
    assert any(_ > 0, [1,2,0])
    assert any(_ < 0, [1,2,0]) == False

def test_one():
    assert one([0, False, 3, ''])
    assert not one([0, False, ''])
    assert not one([1, False, 'a'])
    assert one(_ > 0, [0,1])
    assert not one(_ < 0, [0,1,2])
    assert not one(_ > 0, [0,1,2])

def test_none():
    assert none([0, False])
    assert none(_ < 0, [0, -1]) == False

def test_some():
    assert some([0, '', 2, 3]) == 2
    assert some(_ > 3, range(10)) == 4


def test_flip():
    assert flip({'a':1, 'b':2}) == {1:'a', 2:'b'}

def test_project():
    assert project({'a':1, 'b':2, 'c': 3}, 'ac') == {'a':1, 'c': 3}
    dd = defaultdict(int, {'a':1, 'b':2, 'c': 3})
    assert eq(project(dd, 'ac'), defaultdict(int, {'a':1, 'c': 3}))