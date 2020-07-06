"""Performs all generation transforms on the given dataframe"""

import copy
import json
from csv_to_json.transforms.transform_functions.generation_functions import *


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
            if isinstance(value, dict) and lookup_key in value:
                yield sub_map
            yield from item_generator(value, lookup_key)
    elif isinstance(sub_map, list):
        for list_item in sub_map:
            if isinstance(list_item, dict) and lookup_key in list_item:
                yield sub_map
            yield from item_generator(list_item, lookup_key)


def perform_generation_transforms(mappings, df, output_file, dicts):
    """Performs all generation transforms on the dataframe and outputs"""
    out = open(output_file, 'w')
    for index in df.index:
        mappings_copy = copy.deepcopy(mappings)
        sub_maps = list(item_generator(mappings_copy, 'transforms'))
        for sub_map in filter(lambda x: isinstance(x, dict), sub_maps):
            sub_map_copy = copy.deepcopy(sub_map)
            for key in dict(filter(lambda x: 'transforms' in x[1],
                                   sub_map_copy.items())):
                for transform in filter(lambda x: 'type' in x and x['type'] in
                                        available_transforms,
                                        sub_map_copy[key]['transforms']):
                    available_transforms[transform['type']](
                        sub_map, key, transform, df, index, dicts)
                if key in sub_map and 'transforms' in sub_map[key]:
                    del sub_map[key]['transforms']
        for sub_map in filter(lambda x: isinstance(x, list), sub_maps):
            sub_map_copy = copy.deepcopy(sub_map)
            list_index = 0
            for list_item in filter(lambda x: isinstance(x, dict) and
                                    'transforms' in x, sub_map_copy):
                mapping_size = len(sub_map)
                for transform in filter(lambda x: 'type' in x and
                                        x['type'] in available_transforms,
                                        list_item['transforms']):
                    if not list_index >= len(sub_map):
                        available_transforms[transform['type']](
                            sub_map, list_index, transform, df, index, dicts)
                if (not list_index >= len(sub_map) and
                        'transforms' in sub_map[list_index]):
                    del sub_map[list_index]['transforms']
                if mapping_size == len(sub_map):
                    list_index += 1
        fill_json_values('sourceCol', mappings_copy, df, index)
        out.write(json.dumps(mappings_copy) + '\n')
    out.close()
    return df


available_transforms = {
    'deletion-conditional': deletion_conditional,
    'conditional': standard_conditional,
    'fill-from-dictionary': fill_from_dictionary
}
