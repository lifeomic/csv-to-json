"""Performs all file transforms on the given dataframe"""

from csv_to_json.transforms.transform_functions.file_functions import *


def perform_file_transforms(mappings, df, dicts):
    """Performs all file transforms on the dataframe"""
    if 'file-transforms' not in mappings:
        return (mappings, df, dicts)
    for transform in mappings['file-transforms']:
        if 'type' in transform and transform['type'] in available_transforms:
            df, dicts = available_transforms[transform['type']](
                transform, df, dicts)
    del mappings['file-transforms']
    return (mappings, df, dicts)


available_transforms = {
    'transpose': transpose,
    'dictionary-from-file': dictionary_from_file
}
