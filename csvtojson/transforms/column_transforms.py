import iso8601
import numpy as np
import pandas as pd
from datetime import timedelta
from uuid import uuid4


def default(sub_map, table, source_col, operation_col):
    if not source_col in list(table):
        table[operation_col] = [np.nan for index in table.index]
    default_value = sub_map['defaultValue']
    if default_value in available_default_values:
        default_value = available_default_values[default_value]
        table[operation_col] = table[source_col].transform(
            lambda x: str(default_value()) if pd.isnull(x) else x)
        return table
    table[operation_col] = table[source_col].transform(
        lambda x: default_value if pd.isnull(x) else x)
    return table


def time_delta(sub_map, table, source_col, operation_col):
    base_col = sub_map['baseCol']
    table[operation_col] = table[base_col]
    delta_list = ['days', 'hours']
    for key in (set(delta_list).intersection(key for key in sub_map if (isinstance(sub_map[key], dict) and 'sourceCol' in sub_map[key]))):
        if key == 'days':
            table[operation_col] = table.apply(lambda row: str(iso8601.parse_date(
                row[operation_col]) + timedelta(days=float(row[sub_map[key]['sourceCol']]))) if (not pd.isnull(row[operation_col]) and not pd.isnull(row[sub_map[key]['sourceCol']])) else row[operation_col], axis=1)
        elif key == 'hours':
            table[operation_col] = table.apply(lambda row: str(iso8601.parse_date(
                row[operation_col]) + timedelta(hours=float(row[sub_map[key]['sourceCol']]))) if (not pd.isnull(row[operation_col]) and not pd.isnull(row[sub_map[key]['sourceCol']])) else row[operation_col], axis=1)
    for key in (set(delta_list).intersection(key for key in sub_map if not (isinstance(sub_map[key], dict)))):
        if key == 'days':
            table[operation_col] = table[operation_col].transform(lambda x: str(iso8601.parse_date(
                x) + timedelta(days=sub_map[key])) if (not pd.isnull(x) and not pd.isnull(sub_map[key])) else x)
        elif key == 'hours':
            table[operation_col] = table[operation_col].transform(lambda x: str(iso8601.parse_date(
                x) + timedelta(hours=sub_map[key])) if (not pd.isnull(x) and not pd.isnull(sub_map[key])) else x)
    return table


def trim_whitespace(sub_map, table, source_col, operation_col):
    table[operation_col] = table[operation_col].transform(
        lambda x: x.strip() if not pd.isnull(x) else x)
    return table


def uppercase(sub_map, table, source_col, operation_col):
    table[operation_col] = table[operation_col].transform(
        lambda x: x.upper() if not pd.isnull(x) else x)
    return table


def string_replacement(sub_map, table, source_col, operation_col):
    replacement_string = sub_map['replacementString']
    string_to_replace = sub_map['stringToReplace']
    table[operation_col] = table[operation_col].transform(lambda x: x.replace(
        string_to_replace, replacement_string) if not pd.isnull(x) else x)
    return table


def lowercase(sub_map, table, source_col, operation_col):
    table[operation_col] = table[operation_col].transform(
        lambda x: x.lower() if not pd.isnull(x) else x)
    return table


def format_date(sub_map, table, source_col, operation_col):
    table[operation_col] = table[operation_col].transform(
        lambda x: str(iso8601.parse_date(x)) if not pd.isnull(x) else x)
    return table


def string_concatenation(sub_map, table, source_col, operation_col):
    before_string = sub_map['beforeString'] if 'beforeString' in sub_map else ''
    after_string = sub_map['afterString'] if 'afterString' in sub_map else ''
    table[operation_col] = table[operation_col].transform(
        lambda x: before_string + x + after_string)
    return table


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


def perform_column_transforms(mappings, table):
    sub_maps = list(item_generator(mappings, 'transforms'))
    # this could be simplified greatly by simply looping through all sub_maps that have a valid type
    for sub_map in sub_maps:
        if (len(set(map(lambda transform: transform['type'], sub_map['transforms'])).intersection(available_transforms)) > 0):
            print(sub_map)
            operation_col = source_col = str(uuid4())
            if 'sourceCol' in sub_map:
                source_col = sub_map['sourceCol']
                table[operation_col] = table[source_col]
            else:
                table[operation_col] = [np.nan for index in table.index]
            sub_map.update({'sourceCol': operation_col})
        # this can be simplified to looping through all transforms in available_transforms
        for transform in sub_map['transforms']:
            if 'type' in transform and transform['type'] in available_transforms:
                table = available_transforms[transform['type']](
                    transform, table, source_col, operation_col)
        if not source_col in list(table):
            del sub_map['sourceCol']
    return (mappings, table)


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

available_default_values = {
    'uuid': uuid4
}
