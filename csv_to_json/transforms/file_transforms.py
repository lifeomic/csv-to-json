from transform_functions.file_transforms import *


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
