import iso8601
import numpy as np
import pandas as pd
from datetime import timedelta
from uuid import uuid4


def default(sub_map, df, source_col, op_col):
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
    base_col = sub_map['baseCol']
    df[op_col] = df[base_col]
    deltas = ['days', 'hours']
    for key in (set(deltas).intersection(key for key in sub_map
                                         if (isinstance(sub_map[key], dict) and
                                             'sourceCol' in sub_map[key]))):
        if key == 'days':
            df[op_col] = \
                (df.apply(lambda r:
                          (str(iso8601.parse_date(r[op_col]) +
                               timedelta(
                                   days=float(r[sub_map[key]['sourceCol']])))
                           if (not pd.isnull(r[op_col]) and
                               not pd.isnull(r[sub_map[key]['sourceCol']]))
                              else r[op_col]), axis=1))
        elif key == 'hours':
            df[op_col] = \
                df.apply(lambda r:
                         str(iso8601.parse_date(r[op_col]) +
                             timedelta(
                             hours=float(r[sub_map[key]['sourceCol']])))
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
    df[op_col] = df[op_col].transform(
        lambda x: x.strip() if not pd.isnull(x) else x)
    return df


def string_replacement(sub_map, df, source_col, op_col):
    replacement_string = sub_map['replacementString']
    string_to_replace = sub_map['stringToReplace']
    df[op_col] = df[op_col].transform(lambda x: x.replace(
        string_to_replace, replacement_string) if not pd.isnull(x) else x)
    return df


def uppercase(sub_map, df, source_col, op_col):
    df[op_col] = df[op_col].transform(
        lambda x: x.upper() if not pd.isnull(x) else x)
    return df


def lowercase(sub_map, df, source_col, op_col):
    df[op_col] = df[op_col].transform(
        lambda x: x.lower() if not pd.isnull(x) else x)
    return df


def format_date(sub_map, df, source_col, op_col):
    df[op_col] = df[op_col].transform(
        lambda x: str(iso8601.parse_date(x)) if not pd.isnull(x) else x)
    return df


def string_concatenation(sub_map, df, source_col, op_col):
    before = sub_map['beforeString'] if 'beforeString' in sub_map else ''
    after = sub_map['afterString'] if 'afterString' in sub_map else ''
    df[op_col] = df[op_col].transform(
        lambda x: before + x + after)
    return df


available_default_values = {
    'uuid': uuid4
}
