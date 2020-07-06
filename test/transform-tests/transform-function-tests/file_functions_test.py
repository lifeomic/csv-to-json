import pandas as pd
from csv_to_json.transforms.transform_functions.file_functions import *


def test_transpose():
    df = pd.DataFrame.from_dict(
        {'col_one': ['col_two'], 'cell_one': ['cell_two']})
    df, _ = transpose({}, df, {})
    assert df['col_one'][1] == 'cell_one' and df['col_two'][1] == 'cell_two'


def test_dictionary_from_file():
    transform = {
        'dictionaryName': 'one',
        'inputFile': 'test/data/dictionary.csv',
        'separation': ',',
        'keyCol': 'number',
        'valueCol': 'letter'
    }
    df, test_dict = dictionary_from_file(transform, None, {})
    assert 'one' in test_dict and len(test_dict['one']) == 5
    assert test_dict['one']['1'] == 'a' and test_dict['one']['4'] == 'd'
