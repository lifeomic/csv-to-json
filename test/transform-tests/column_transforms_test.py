import pandas as pd

import csvtojson.transforms.column_transforms as column_transforms

def test_default():
    table = pd.DataFrame.from_dict({'generic_string': ['foo', None]})
    sub_map = {'defaultValue': 'bar'}
    table['operation_col'] = table['generic_string']
    table = column_transforms.default(sub_map, table, 'generic_string', 'operation_col')
    assert(list(table['generic_string']) == ['foo', None])
    assert(list(table['operation_col']) == ['foo', 'bar'])


def test_default_uuid():
    table = pd.DataFrame({'col_for_index': ['index']})
    sub_map = {'defaultValue': 'uuid'}
    table = column_transforms.default(sub_map, table, 'source_col', 'operation_col')
    assert(not pd.isnull(table['operation_col'][0]) and len(table['operation_col'][0]) == 36)


def test_time_delta():
    table = pd.DataFrame.from_dict({'base_time': ['1988-7-8 07:22'], 'day_shift': ['5']})
    sub_map = {'baseCol': 'base_time', 'days': {'sourceCol': 'day_shift'}, 'hours': 3}
    table = column_transforms.time_delta(sub_map, table, None, 'operation_col')
    assert(table['base_time'][0] == '1988-7-8 07:22' and table['day_shift'][0] == '5')
    assert(table['operation_col'][0] == '1988-07-13 10:22:00+00:00')


def test_trim_whitespace():
    table = pd.DataFrame.from_dict({'whitespace_words': ['     wordone      ', 'wordtwo']})
    table['operation_col'] = table['whitespace_words']
    table = column_transforms.trim_whitespace({}, table, 'whitespace_words', 'operation_col')
    assert(list(table['whitespace_words']) == ['     wordone      ', 'wordtwo'])
    assert(list(table['operation_col']) == ['wordone', 'wordtwo'])


def test_uppercase():
    table = pd.DataFrame.from_dict({'lowercase_words': ['word ONE']})
    table['operation_col'] = table['lowercase_words']
    table = column_transforms.uppercase({}, table, 'lowercase_words', 'operation_col')
    assert(table['lowercase_words'][0] == 'word ONE')
    assert(table['operation_col'][0] == 'WORD ONE')


def test_lowercase():
    table = pd.DataFrame.from_dict({'uppercase_words': ['WORD one']})
    table['operation_col'] = table['uppercase_words']
    table = column_transforms.lowercase({}, table, 'uppercase_words', 'operation_col')
    assert(table['uppercase_words'][0] == 'WORD one')
    assert(table['operation_col'][0] == 'word one')


def test_format_date():
    table = pd.DataFrame.from_dict({'unformatted_date': ['1988-7-8 07:22']})
    table['operation_col'] = table['unformatted_date']
    table = column_transforms.format_date({}, table, 'unformatted_date', 'operation_col')
    assert(table['unformatted_date'][0] == '1988-7-8 07:22')
    assert(table['operation_col'][0] == '1988-07-08 07:22:00+00:00')


def test_string_concatenation():
    table = pd.DataFrame.from_dict({'generic_string': ['foo']})
    sub_map = {'beforeString': 'bar ', 'afterString': ' baz'}
    table['operation_col'] = table['generic_string']
    table = column_transforms.string_concatenation(sub_map, table, 'generic_string', 'operation_col')
    assert(table['generic_string'][0] == 'foo')
    assert(table['operation_col'][0] == 'bar foo baz')