import pandas as pd
from csv_to_json.transforms.transform_functions.file_functions import *


def test_transpose():
    df = pd.DataFrame.from_dict(
        {'col_one': ['col_two'], 'cell_one': ['cell_two']})
    df = transpose({}, df)
    assert(df['col_one'][1] == 'cell_one' and df['col_two'][1] == 'cell_two')
