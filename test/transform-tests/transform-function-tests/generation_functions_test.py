import pandas as pd
from csv_to_json.transforms.transform_functions.generation_functions import *


def test_deletion_conditional():
    df = pd.DataFrame.from_dict({'value_one': ['foo']})
    mapping = {'key': 'bar'}
    conditional = {
        'type': 'deletion-conditional',
        'condition': 'eq',
        'sourceCol': 'value_one',
        'compareTo': 'foo'
    }
    deletion_conditional(mapping, 'key', conditional, df, 0)
    assert('key' in mapping and mapping['key'] == 'bar')
    df = pd.DataFrame.from_dict({'value_one': ['bar']})
    deletion_conditional(mapping, 'key', conditional, df, 0)
    assert(not mapping and 'key' not in mapping)


def test_conditional_equal():
    assert(conditional_equal(3, 3))
    assert(conditional_equal('foo', 'foo'))
    assert(not conditional_equal(4, 3))
    assert(not conditional_equal('foo', 'bar'))
    assert(conditional_equal(None, 'empty'))
    assert(not conditional_equal(3, 'empty'))
    assert(conditional_equal(3, 'occupied'))
    assert(not conditional_equal(None, 'occupied'))


def test_conditional_not_equal():
    assert(not available_conditionals['not-eq'](3, 3))
    assert(available_conditionals['not-eq']('foo', 'bar'))
    assert(available_conditionals['not-eq'](None, 'occupied'))


def test_conditional_less_than():
    assert(conditional_less_than(2, 3))
    assert(not conditional_less_than(3.5, 2.4))


def test_conditional_not_less_than():
    assert(not available_conditionals['not-less-than'](2, 3))
    assert(available_conditionals['not-less-than'](3.5, 2.4))


def test_conditional_greater_than():
    assert(conditional_greater_than(3, 2))
    assert(not conditional_greater_than(2.4, 3.5))


def test_conditional_not_greater_than():
    assert(not available_conditionals['not-greater-than'](3, 2))
    assert(available_conditionals['not-greater-than'](2.4, 3.5))


def test_conditional_less_than_or_equal_to():
    assert(conditional_less_than_or_equal_to(2, 3))
    assert(conditional_less_than_or_equal_to(3, 3))
    assert(not(conditional_less_than_or_equal_to(4.5, 3)))


def test_conditional_not_less_than_or_equal_to():
    assert(available_conditionals['not-less-than-or-equal-to'](4.5, 3))
    assert(not available_conditionals['not-less-than-or-equal-to'](3, 3))
    assert(not available_conditionals['not-less-than-or-equal-to'](2, 3))


def test_conditional_greater_than_or_equal_to():
    assert(conditional_greater_than_or_equal_to(3, 2))
    assert(conditional_greater_than_or_equal_to(3, 3))
    assert(not conditional_greater_than_or_equal_to(3, 4.5))


def test_conditional_not_greater_than_or_equal_to():
    assert(available_conditionals['not-greater-than-or-equal-to'](3, 4.5))
    assert(not available_conditionals['not-greater-than-or-equal-to'](3, 3))
    assert(not available_conditionals['not-greater-than-or-equal-to'](3, 2))


def test_empty():
    assert(empty(None))
    assert(not empty('foo'))


def test_occupied():
    assert(occupied('foo'))
    assert(not occupied(None))
