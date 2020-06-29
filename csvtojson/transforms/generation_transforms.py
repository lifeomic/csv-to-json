import copy
import json
import pandas as pd


def handle_conditional(conditional, table, index):
    if 'condition' in conditional and conditional['condition'] in available_conditionals:
        condition_function = available_conditionals[conditional['condition']]
        cell_value = table[conditional['sourceCol']][index]
        comparison = conditional['compareTo']
        return condition_function(cell_value, comparison)


def handle_conditional_value(mapping, key, conditional, table, index, value):
    if not key in mapping:
        return
    if (isinstance(conditional['values'][value], dict) and 'sourceCol' in conditional['values'][value]):
        mapping['sourceCol'] = conditional['values'][value]['sourceCol']
    else:
        string_value = conditional['values'][value]
        del mapping[key]['transforms']
        mapping[key] = string_value


def deletion_conditional(mapping, key, conditional, table, index):
    if not handle_conditional(conditional, table, index) and (isinstance(mapping, list) or (isinstance(mapping, dict) and key in mapping)):
        del mapping[key]


def conditional(mapping, key, conditional, table, index):
    if handle_conditional(conditional, table, index):
        handle_conditional_value(
            mapping, key, conditional, table, index, 'true')
    else:
        handle_conditional_value(
            mapping, key, conditional, table, index, 'false')


def conditional_equal(cell_value, comparison):
    if comparison in available_comparison_values:
        return available_comparison_values[comparison](cell_value)
    return cell_value == comparison


def conditional_less_than(cell_value, comparison):
    return float(cell_value) < float(comparison)


def conditional_greater_than(cell_value, comparison):
    return float(cell_value) > float(comparison)


def conditional_less_than_or_equal_to(cell_value, comparison):
    return float(cell_value) <= float(comparison)


def conditional_greater_than_or_equal_to(cell_value, comparison):
    return float(cell_value) >= float(comparison)


def empty(cell_value):
    return pd.isnull(cell_value)


def occupied(cell_value):
    return not pd.isnull(cell_value)


def fill_json_values(lookup_key, var, table, index):
    for key, value in var.items():
        if isinstance(value, dict):
            if lookup_key in value:
                var[key] = table[value[lookup_key]][index]
            fill_json_values(lookup_key, value, table, index)
        elif isinstance(value, list):
            for list_item in value:
                fill_json_values(lookup_key, list_item, table, index)


def item_generator(sub_map, lookup_key):
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


def perform_generation_transforms(mappings, table, output_file):
    with open(output_file, 'w') as o:
        for index in table.index:
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
                                        sub_map, key, transform, table, index)
                            if key in sub_map and 'transforms' in sub_map[key]:
                                del sub_map[key]['transforms']
                elif (isinstance(sub_map_copy, list)):
                    list_index = 0
                    for list_item in sub_map_copy:
                        mapping_size = len(sub_map)
                        if (isinstance(list_item, dict)) and 'transforms' in list_item:
                            for transform in list_item['transforms']:
                                if 'type' in transform and transform['type'] in available_transforms and not list_index >= len(sub_map):
                                    available_transforms[transform['type']](
                                        sub_map, list_index, transform, table, index)
                            if not list_index >= len(sub_map) and 'transforms' in sub_map[list_index]:
                                del sub_map[list_index]['transforms']
                        if mapping_size == len(sub_map):
                            list_index += 1
            fill_json_values('sourceCol', mappings_copy, table, index)
            o.write(json.dumps(mappings_copy) + '\n')
    return table


available_transforms = {
    'deletion-conditional': deletion_conditional,
    'conditional': conditional
}

available_comparison_values = {
    'empty': empty,
    'occupied': occupied
}

available_conditionals = {
    'eq': conditional_equal,
    'less-than': conditional_less_than,
    'greater-than': conditional_greater_than,
    'less-than-or-equal-to': conditional_less_than_or_equal_to,
    'greater-than-or-equal-to': conditional_greater_than_or_equal_to
}
