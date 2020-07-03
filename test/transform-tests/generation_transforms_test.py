import pandas as pd
from csv_to_json.transforms.generation_transforms import *


def test_item_generator():
    mapping = {
        'foo': {
            'baz': {
                'lookup_key': 'foo'
            }
        },
        'bar': [
            {
                'lookup_key': 'foo'
            },
            {
                'false_key': 'bar'
            }
        ],
        'baz': {
            'false_key': 'baz'
        }
    }
    sub_maps = list(item_generator(mapping, 'lookup_key'))
    assert len(sub_maps) == 2
    for sub_map in sub_maps:
        if (isinstance(sub_map, list)):
            assert sub_map[0]['lookup_key'] == 'foo'
            assert sub_map[1]['false_key'] == 'bar'
        else:
            assert sub_map['baz']['lookup_key'] == 'foo'


def test_fill_json_values():
    mapping = {
        'foo': {
            'sourceCol': 'col_one'
        },
        'bar': [
            {
                'baz': {
                    'sourceCol': 'col_two'
                }
            }
        ]
    }
    df = pd.DataFrame.from_dict({'col_one': ['1', '3'], 'col_two': ['2', '4']})
    fill_json_values('sourceCol', mapping, df, 1)
    assert mapping['foo'] == '3'
    assert mapping['bar'][0]['baz'] == '4'
