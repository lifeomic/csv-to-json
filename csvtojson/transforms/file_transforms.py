import pandas as pd

def transpose(transform, table):
    table = table.reset_index().set_index('index').T.reset_index()
    table.columns = table.iloc[0]
    return table[1:]

def perform_file_transforms(mappings, table):
    if not 'file-transforms' in mappings:
        return (mappings, table)
    for transform in mappings['file-transforms']:
        if 'type' in transform and transform['type'] in available_transforms:
            table = available_transforms[transform['type']](transform, table)
    del mappings['file-transforms']
    return (mappings, table)

available_transforms = {
    'transpose': transpose
}