"""Functions for each type of file transform"""

import pandas as pd


def transpose(transform, df, dicts):
    """Transposes the given dataframe"""
    df = df.reset_index().set_index('index').T.reset_index()
    df.columns = df.iloc[0]
    return (df[1:], dicts)


def dictionary_from_file(transform, df, dicts):
    """Creates a dictionary from the supplied transform"""
    name = transform['dictionaryName']
    input_file = transform['inputFile']
    separation = transform['separation'] if 'separation' in transform else ','
    key_col = transform['keyCol']
    value_col = transform['valueCol']
    input_df = pd.read_csv(input_file, dtype='str', sep=separation)
    dicts[name] = dict(zip(input_df[key_col], input_df[value_col]))
    return (df, dicts)
