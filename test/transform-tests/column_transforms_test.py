from csv_to_json.transforms.column_transforms import *


def test_item_generator():
    mapping = {
        'foo': {
            'lookup_key': 'foo'
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
        if 'foo' in sub_map:
            assert 'lookup_key' in sub_map['foo']
        else:
            assert 'lookup_key' in sub_map
