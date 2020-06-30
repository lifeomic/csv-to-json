def transpose(transform, df):
    df = df.reset_index().set_index('index').T.reset_index()
    df.columns = df.iloc[0]
    return df[1:]


def perform_file_transforms(mappings, df):
    if 'file-transforms' not in mappings:
        return (mappings, df)
    for transform in mappings['file-transforms']:
        if 'type' in transform and transform['type'] in available_transforms:
            df = available_transforms[transform['type']](transform, df)
    del mappings['file-transforms']
    return (mappings, df)


available_transforms = {
    'transpose': transpose
}
