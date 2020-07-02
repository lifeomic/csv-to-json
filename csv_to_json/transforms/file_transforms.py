"""Performs all file transforms on the given dataframe"""

from transform_functions.file_transforms import *


def perform_file_transforms(mappings, df):
    """Performs all file transforms on the dataframe"""
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
