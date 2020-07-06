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
    deletion_conditional(mapping, 'key', conditional, df, 0, {})
    assert 'key' in mapping and mapping['key'] == 'bar'
    df = pd.DataFrame.from_dict({'value_one': ['bar']})
    deletion_conditional(mapping, 'key', conditional, df, 0, {})
    assert not mapping and 'key' not in mapping


def test_standard_conditional():
    df = pd.DataFrame.from_dict({'value_one': ['foo']})
    mapping = {
        'value': {
            'transforms': [
                {
                    'type': 'conditional',
                    'condition': 'eq',
                    'sourceCol': 'value_one',
                    'compareTo': 'foo',
                    'values': {
                        'true': 'bar',
                        'false': {
                            'sourceCol': 'fill_in_value'
                        }
                    }
                }
            ]
        }
    }
    standard_conditional(
        mapping, 'value', mapping['value']['transforms'][0], df, 0, {})
    assert mapping['value'] == 'bar'
    df = pd.DataFrame.from_dict(
        {'value_one': ['bar'], 'fill_in_value': ['baz']})
    mapping = {
        'value': {
            'transforms': [
                {
                    'type': 'conditional',
                    'condition': 'eq',
                    'sourceCol': 'value_one',
                    'compareTo': 'foo',
                    'values': {
                        'true': 'bar',
                        'false': {
                            'sourceCol': 'fill_in_value'
                        }
                    }
                }
            ]
        }
    }
    standard_conditional(
        mapping, 'value', mapping['value']['transforms'][0], df, 0, {})
    assert ('sourceCol' in mapping['value'] and
            mapping['value']['sourceCol'] == 'fill_in_value')


def test_check_conditional():
    df = pd.DataFrame.from_dict({'value_one': ['4']})
    conditional = {
        'type': 'conditional',
        'condition': 'not-less-than',
        'sourceCol': 'value_one',
        'compareTo': '3'
    }
    assert check_conditional(conditional, df, 0)
    df = pd.DataFrame.from_dict({'value_one': ['2']})
    assert not check_conditional(conditional, df, 0)


def test_handle_conditional_value():
    mapping = {
        'value': {
            'transforms': [
                {
                    'type': 'conditional',
                    'condition': 'eq',
                    'sourceCol': 'value_one',
                    'compareTo': 'foo',
                    'values': {
                        'true': 'bar',
                        'false': {
                            'sourceCol': 'fill_in_value'
                        }
                    }
                }
            ]
        }
    }
    handle_conditional_value(
        mapping, 'value', mapping['value']['transforms'][0], 'true')
    assert mapping['value'] == 'bar'
    mapping = {
        'value': {
            'transforms': [
                {
                    'type': 'conditional',
                    'condition': 'eq',
                    'sourceCol': 'value_one',
                    'compareTo': 'foo',
                    'values': {
                        'true': 'bar',
                        'false': {
                            'sourceCol': 'fill_in_value'
                        }
                    }
                }
            ]
        }
    }
    handle_conditional_value(
        mapping, 'value', mapping['value']['transforms'][0], 'false')
    assert ('sourceCol' in mapping['value'] and
            mapping['value']['sourceCol'] == 'fill_in_value')


def test_conditional_equal():
    assert conditional_equal(3, 3)
    assert conditional_equal('foo', 'foo')
    assert not conditional_equal(4, 3)
    assert not conditional_equal('foo', 'bar')
    assert conditional_equal(None, 'empty')
    assert not conditional_equal(3, 'empty')
    assert conditional_equal(3, 'occupied')
    assert not conditional_equal(None, 'occupied')


def test_conditional_not_equal():
    assert not available_conditionals['not-eq'](3, 3)
    assert available_conditionals['not-eq']('foo', 'bar')
    assert available_conditionals['not-eq'](None, 'occupied')


def test_conditional_less_than():
    assert conditional_less_than(2, 3)
    assert not conditional_less_than(3.5, 2.4)


def test_conditional_not_less_than():
    assert not available_conditionals['not-less-than'](2, 3)
    assert available_conditionals['not-less-than'](3.5, 2.4)


def test_conditional_greater_than():
    assert conditional_greater_than(3, 2)
    assert not conditional_greater_than(2.4, 3.5)


def test_conditional_not_greater_than():
    assert not available_conditionals['not-greater-than'](3, 2)
    assert available_conditionals['not-greater-than'](2.4, 3.5)


def test_conditional_less_than_or_equal_to():
    assert conditional_less_than_or_equal_to(2, 3)
    assert conditional_less_than_or_equal_to(3, 3)
    assert not(conditional_less_than_or_equal_to(4.5, 3))


def test_conditional_not_less_than_or_equal_to():
    assert available_conditionals['not-less-than-or-equal-to'](4.5, 3)
    assert not available_conditionals['not-less-than-or-equal-to'](3, 3)
    assert not available_conditionals['not-less-than-or-equal-to'](2, 3)


def test_conditional_greater_than_or_equal_to():
    assert conditional_greater_than_or_equal_to(3, 2)
    assert conditional_greater_than_or_equal_to(3, 3)
    assert not conditional_greater_than_or_equal_to(3, 4.5)


def test_conditional_not_greater_than_or_equal_to():
    assert available_conditionals['not-greater-than-or-equal-to'](3, 4.5)
    assert not available_conditionals['not-greater-than-or-equal-to'](3, 3)
    assert not available_conditionals['not-greater-than-or-equal-to'](3, 2)


def test_empty():
    assert empty(None)
    assert not empty('foo')


def test_occupied():
    assert occupied('foo')
    assert not occupied(None)


def test_fill_from_dictionary():
    df = pd.DataFrame.from_dict({'col_one': ['foo']})
    dicts = {'dict_one': {'foo': 'bar', 'bar': 'baz'}}
    mapping = {
        'test_value': {
            'transforms': [
                {
                    'type': 'fill-from-dictionary',
                    'key': {
                        'sourceCol': 'col_one'
                    },
                    'dictionaryName': 'dict_one'
                }
            ]
        }
    }
    fill_from_dictionary(mapping, 'test_value',
                         mapping['test_value']['transforms'][0], df, 0, dicts)
    assert mapping['test_value'] == 'bar'
