import numpy as np
from uuid import uuid4
from transform_functions.column_functions import *


def item_generator(sub_map, lookup_key):
    if isinstance(sub_map, dict):
        for key, value in sub_map.items():
            if key == lookup_key:
                yield sub_map
            else:
                yield from item_generator(value, lookup_key)
    elif isinstance(sub_map, list):
        for obj in sub_map:
            yield from item_generator(obj, lookup_key)


def perform_column_transforms(mappings, df):
    sub_maps = list(item_generator(mappings, 'transforms'))
    for sub_map in sub_maps:
        if (len(set(map(lambda transform: transform['type'],
                        sub_map['transforms'])).intersection(available_transforms)) > 0):
            op_col = source_col = str(uuid4())
            if 'sourceCol' in sub_map:
                source_col = sub_map['sourceCol']
                df[op_col] = df[source_col]
            else:
                df[op_col] = [np.nan for index in df.index]
            sub_map.update({'sourceCol': op_col})
        for transform in sub_map['transforms']:
            if 'type' in transform and transform['type'] in available_transforms:
                df = available_transforms[transform['type']](
                    transform, df, source_col, op_col)
        if source_col not in list(df):
            del sub_map['sourceCol']
    return (mappings, df)


available_transforms = {
    'default': default,
    'trim-whitespace': trim_whitespace,
    'uppercase': uppercase,
    'lowercase': lowercase,
    'string-replacement': string_replacement,
    'string-concatenation': string_concatenation,
    'time-delta': time_delta,
    'format-date': format_date
}
