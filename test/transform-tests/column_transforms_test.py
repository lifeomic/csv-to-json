import pandas as pd

import csvtojson.transforms.column_transforms as column_transforms

def test_trim_whitespace():
    table = pd.DataFrame.from_dict({'whitespace_words': ['     wordone      ', 'wordtwo']})
    sub_map = {'testvalue': {'sourceCol': 'whitespace_words'}}
    table['operation_col'] = table['whitespace_words']
    table = column_transforms.trim_whitespace(sub_map, table, 'whitespace_words', 'operation_col')
    assert(table['whitespace_words'][0] == '     wordone      ' and table['whitespace_words'][1] == 'wordtwo')
    assert(table['operation_col'][0] == 'wordone' and table['whitespace_words'][1] == 'wordtwo')