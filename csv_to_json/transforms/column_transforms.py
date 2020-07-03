"""Performs all column transformations upon the given dataframe"""

from uuid import uuid4
import numpy as np
from csv_to_json.transforms.transform_functions.column_functions import *


def item_generator(sub_map, lookup_key):
    """Returns all dictionaries containing the lookup key"""
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
    """Performs all column transforms in the mapping on the dataframe"""
    sub_maps = list(item_generator(mappings, 'transforms'))
    for sub_map in sub_maps:
        if (len(set(map(lambda transform: transform['type'],
                        sub_map['transforms']))
                .intersection(available_transforms)) > 0):
            op_col = source_col = str(uuid4())
            if 'sourceCol' in sub_map:
                source_col = sub_map['sourceCol']
                df[op_col] = df[source_col]
            else:
                df[op_col] = [np.nan for index in df.index]
            sub_map.update({'sourceCol': op_col})
        filtered_transforms = filter(lambda x: (
            'type' in x and
            x['type'] in available_transforms), sub_map['transforms'])
        for transform in filtered_transforms:
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
    'substring': substring,
    'string-replacement': string_replacement,
    'string-concatenation': string_concatenation,
    'time-delta': time_delta,
    'format-date': format_date
}
