def transpose(transform, df):
    """Transposes the given dataframe"""
    df = df.reset_index().set_index('index').T.reset_index()
    df.columns = df.iloc[0]
    return df[1:]
