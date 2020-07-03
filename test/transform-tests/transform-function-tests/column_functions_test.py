import pandas as pd
from csv_to_json.transforms.transform_functions.column_functions import *


def test_default():
    df = pd.DataFrame.from_dict({'generic_string': ['foo', None]})
    sub_map = {'defaultValue': 'bar'}
    df['operation_col'] = df['generic_string']
    df = default(
        sub_map, df, 'generic_string', 'operation_col')
    assert list(df['generic_string']) == ['foo', None]
    assert list(df['operation_col']) == ['foo', 'bar']


def test_default_uuid():
    df = pd.DataFrame({'col_for_index': ['index']})
    sub_map = {'defaultValue': 'uuid'}
    df = default(
        sub_map, df, 'source_col', 'operation_col')
    assert (not pd.isnull(df['operation_col'][0]) and
            len(df['operation_col'][0]) == 36)


def test_time_delta():
    df = pd.DataFrame.from_dict(
        {'base_time': ['1988-7-8 07:22'], 'day_shift': ['5']})
    sub_map = {'baseCol': 'base_time', 'days': {
        'sourceCol': 'day_shift'}, 'hours': 3}
    df = time_delta(sub_map, df, None, 'operation_col')
    assert (df['base_time'][0] ==
            '1988-7-8 07:22' and df['day_shift'][0] == '5')
    assert df['operation_col'][0] == '1988-07-13 10:22:00+00:00'


def test_trim_whitespace():
    df = pd.DataFrame.from_dict(
        {'whitespace_words': ['     wordone      ', 'wordtwo']})
    df['operation_col'] = df['whitespace_words']
    df = trim_whitespace(
        {}, df, 'whitespace_words', 'operation_col')
    assert (list(df['whitespace_words']) ==
            ['     wordone      ', 'wordtwo'])
    assert list(df['operation_col']) == ['wordone', 'wordtwo']


def test_uppercase():
    df = pd.DataFrame.from_dict({'lowercase_words': ['word ONE']})
    df['operation_col'] = df['lowercase_words']
    df = uppercase(
        {}, df, 'lowercase_words', 'operation_col')
    assert df['lowercase_words'][0] == 'word ONE'
    assert df['operation_col'][0] == 'WORD ONE'


def test_lowercase():
    df = pd.DataFrame.from_dict({'uppercase_words': ['WORD one']})
    df['operation_col'] = df['uppercase_words']
    df = lowercase(
        {}, df, 'uppercase_words', 'operation_col')
    assert df['uppercase_words'][0] == 'WORD one'
    assert df['operation_col'][0] == 'word one'


def test_format_date():
    df = pd.DataFrame.from_dict({'unformatted_date': ['1988-7-8 07:22']})
    df['operation_col'] = df['unformatted_date']
    df = format_date(
        {}, df, 'unformatted_date', 'operation_col')
    assert df['unformatted_date'][0] == '1988-7-8 07:22'
    assert df['operation_col'][0] == '1988-07-08 07:22:00+00:00'


def test_string_concatenation():
    df = pd.DataFrame.from_dict({'generic_string': ['foo']})
    sub_map = {'beforeString': 'bar ', 'afterString': ' baz'}
    df['operation_col'] = df['generic_string']
    df = string_concatenation(
        sub_map, df, 'generic_string', 'operation_col')
    assert df['generic_string'][0] == 'foo'
    assert df['operation_col'][0] == 'bar foo baz'


def test_substring():
    df = pd.DataFrame.from_dict({'full_string': ['long string']})
    df['operation_col'] = df['full_string']
    sub_map = {'startIndex': '1', 'endIndex': '4'}
    df = substring(sub_map, df, 'full_string', 'operation_col')
    assert df['full_string'][0] == 'long string'
    assert df['operation_col'][0] == 'ong'
    df['operation_col'] = df['full_string']
    sub_map = {'startIndex': '5'}
    df = substring(sub_map, df, 'full_string', 'operation_col')
    assert df['operation_col'][0] == 'string'
    df['operation_col'] = df['full_string']
    sub_map = {'endIndex': '4'}
    df = substring(sub_map, df, 'full_string', 'operation_col')
    assert df['operation_col'][0] == 'long'
