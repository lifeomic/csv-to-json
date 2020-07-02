import copy
import json
from transform_functions.generation_transforms import *


def fill_json_values(lookup_key, var, df, index):
    """Recursively builds and returns each JSON object from the mappings"""
    for key, value in var.items():
        if isinstance(value, dict):
            if lookup_key in value:
                var[key] = df[value[lookup_key]][index]
            fill_json_values(lookup_key, value, df, index)
        elif isinstance(value, list):
            for list_item in value:
                fill_json_values(lookup_key, list_item, df, index)


def item_generator(sub_map, lookup_key):
    """Returns all objects with dictionaries that contain the lookup key"""
    if isinstance(sub_map, dict):
        for _, value in sub_map.items():
            if lookup_key in value:
                yield sub_map
            yield from item_generator(value, lookup_key)
    elif isinstance(sub_map, list):
        for list_item in sub_map:
            if isinstance(list_item, dict) and lookup_key in list_item:
                yield sub_map
            yield from item_generator(list_item, lookup_key)


def perform_generation_transforms(mappings, df, output_file):
    """Performs all generation transforms on the dataframe and outputs"""
    with open(output_file, 'w') as out:
        for index in df.index:
            mappings_copy = copy.deepcopy(mappings)
            sub_maps = list(item_generator(mappings_copy, 'transforms'))
            for sub_map in sub_maps:
                sub_map_copy = copy.deepcopy(sub_map)
                if (isinstance(sub_map_copy, dict)):
                    for key in sub_map_copy:
                        if 'transforms' in sub_map[key]:
                            for transform in sub_map[key]['transforms']:
                                if 'type' in transform and transform['type'] in available_transforms:
                                    available_transforms[transform['type']](
                                        sub_map, key, transform, df, index)
                            if key in sub_map and 'transforms' in sub_map[key]:
                                del sub_map[key]['transforms']
                elif (isinstance(sub_map_copy, list)):
                    list_index = 0
                    for list_item in sub_map_copy:
                        mapping_size = len(sub_map)
                        if (isinstance(list_item, dict)) and 'transforms' in list_item:
                            for transform in list_item['transforms']:
                                if ('type' in transform and transform['type'] in available_transforms and
                                        not list_index >= len(sub_map)):
                                    available_transforms[transform['type']](
                                        sub_map, list_index, transform, df, index)
                            if not list_index >= len(sub_map) and 'transforms' in sub_map[list_index]:
                                del sub_map[list_index]['transforms']
                        if mapping_size == len(sub_map):
                            list_index += 1
            fill_json_values('sourceCol', mappings_copy, df, index)
            out.write(json.dumps(mappings_copy) + '\n')
    return df


available_transforms = {
    'deletion-conditional': deletion_conditional,
    'conditional': standard_conditional
}
