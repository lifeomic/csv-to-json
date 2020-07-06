"""Functions for each type of column transform"""

from datetime import timedelta
from uuid import uuid4
import iso8601
import numpy as np
import pandas as pd


def default(sub_map, df, source_col, op_col):
    """Sets all empty values in a column to the default value"""
    if source_col not in list(df):
        df[op_col] = [np.nan for index in df.index]
    default_value = sub_map['defaultValue']
    if default_value in available_default_values:
        default_value = available_default_values[default_value]
        df[op_col] = df[op_col].transform(
            lambda x: str(default_value()) if pd.isnull(x) else x)
        return df
    df[op_col] = df[source_col].transform(
        lambda x: default_value if pd.isnull(x) else x)
    return df


def time_delta(sub_map, df, source_col, op_col):
    """Creates a time delta column based on the given numbers"""
    base_col = sub_map['baseCol']
    df[op_col] = df[base_col]
    deltas = ['days', 'hours']
    key = None
    for key in (set(deltas)
                .intersection(
                    k for k in sub_map if (isinstance(sub_map[k], dict) and
                                           'sourceCol' in sub_map[k]))):
        # pylint: disable=undefined-loop-variable
        if key == 'days':
            df[op_col] = \
                (df.apply(lambda r:
                          (str(iso8601.parse_date(r[op_col]) +
                               timedelta(days=float(
                                   r[sub_map[key]['sourceCol']])))
                           if (not pd.isnull(r[op_col]) and
                               not pd.isnull(r[sub_map[key]['sourceCol']]))
                           else r[op_col]), axis=1))
        elif key == 'hours':
            df[op_col] = \
                df.apply(lambda r:
                         str(iso8601.parse_date(r[op_col]) +
                             timedelta(hours=float(
                                 r[sub_map[key]['sourceCol']])))
                         if (not pd.isnull(r[op_col]) and
                             not pd.isnull(r[sub_map[key]['sourceCol']]))
                         else r[op_col], axis=1)
    for key in (set(deltas).intersection(key for key in sub_map if not
                                         (isinstance(sub_map[key], dict)))):
        if key == 'days':
            df[op_col] = (df[op_col]
                          .transform(lambda x:
                                     str(iso8601.parse_date(x) +
                                         timedelta(days=sub_map[key]))
                                     if (not pd.isnull(x) and not
                                         pd.isnull(sub_map[key])) else x))
        elif key == 'hours':
            df[op_col] = (df[op_col]
                          .transform(lambda x:
                                     str(iso8601.parse_date(x) +
                                         timedelta(hours=sub_map[key]))
                                     if (not pd.isnull(x) and not
                                         pd.isnull(sub_map[key])) else x))
    return df


def trim_whitespace(sub_map, df, source_col, op_col):
    """Trims whitespace on all values in the column"""
    df[op_col] = df[op_col].transform(
        lambda x: x.strip() if not pd.isnull(x) else x)
    return df


def string_replacement(sub_map, df, source_col, op_col):
    """Performs a string replacement on all values in the column"""
    replacement_string = sub_map['replacementString']
    string_to_replace = sub_map['stringToReplace']
    df[op_col] = df[op_col].transform(lambda x: x.replace(
        string_to_replace, replacement_string) if not pd.isnull(x) else x)
    return df


def uppercase(sub_map, df, source_col, op_col):
    """Capitizes all letters in the column"""
    df[op_col] = df[op_col].transform(
        lambda x: x.upper() if not pd.isnull(x) else x)
    return df


def lowercase(sub_map, df, source_col, op_col):
    """Sets all lets in the column to lowercase"""
    df[op_col] = df[op_col].transform(
        lambda x: x.lower() if not pd.isnull(x) else x)
    return df


def format_date(sub_map, df, source_col, op_col):
    """Formats all dates in the column to iso8601"""
    df[op_col] = df[op_col].transform(
        lambda x: str(iso8601.parse_date(x)) if not pd.isnull(x) else x)
    return df


def string_concatenation(sub_map, df, source_col, op_col):
    """Adds the before string and after string to all values in the column"""
    before = sub_map['beforeString'] if 'beforeString' in sub_map else ''
    after = sub_map['afterString'] if 'afterString' in sub_map else ''
    df[op_col] = df[op_col].transform(
        lambda x: before + x + after)
    return df


def substring(sub_map, df, source_col, op_col):
    """Takes a substring of every string in the column"""
    start_index = int(sub_map['startIndex']
                      ) if 'startIndex' in sub_map else 0
    end_index = int(sub_map['endIndex']) if 'endIndex' in sub_map else None
    df[op_col] = df[op_col].transform(
        lambda x: x[start_index:end_index] if not pd.isnull(x) else x)
    return df


available_default_values = {
    'uuid': uuid4
}
