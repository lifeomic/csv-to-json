"""Functions for each type of generation transform"""

import pandas as pd


def deletion_conditional(mapping, key, conditional, df, index, dicts):
    """Deletes the given key from the mapping if the condition is false"""
    if (not check_conditional(conditional, df, index) and
            (isinstance(mapping, list) or (isinstance(mapping, dict) and
                                           key in mapping))):
        del mapping[key]


def standard_conditional(mapping, key, conditional, df, index, dicts):
    """Sets the given key from the mapping to the true value if
       true or to the false value if false"""
    if check_conditional(conditional, df, index):
        handle_conditional_value(
            mapping, key, conditional, 'true')
    else:
        handle_conditional_value(
            mapping, key, conditional, 'false')


def check_conditional(conditional, df, index):
    """Evalutates the conditional, returning true or false"""
    if ('condition' in conditional and
            conditional['condition'] in available_conditionals):
        condition_function = available_conditionals[conditional['condition']]
        cell_value = df[conditional['sourceCol']][index]
        comparison = conditional['compareTo']
        return condition_function(cell_value, comparison)
    return False


def handle_conditional_value(mapping, key, conditional, value):
    """Handles the remapping based on the outcome of the conditional"""
    if key not in mapping:
        return
    if (isinstance(conditional['values'][value], dict) and
            'sourceCol' in conditional['values'][value]):
        mapping[key]['sourceCol'] = conditional['values'][value]['sourceCol']
        del mapping[key]['transforms']
    else:
        string_value = conditional['values'][value]
        del mapping[key]['transforms']
        mapping[key] = string_value


def conditional_equal(cell_value, comparison):
    """Returns true if the two values are equal, false otherwise"""
    if comparison in available_comparison_values:
        return available_comparison_values[comparison](cell_value)
    return cell_value == comparison


def conditional_less_than(cell_value, comparison):
    """Returns true if the cell value is less than the comparison,
       false otherwise"""
    return float(cell_value) < float(comparison)


def conditional_greater_than(cell_value, comparison):
    """Returns true if the cell value is greater than the comparison,
       false otherwise"""
    return float(cell_value) > float(comparison)


def conditional_less_than_or_equal_to(cell_value, comparison):
    """Returns true if the cell value is less than or equal to
       the comparison, false otherwise"""
    return float(cell_value) <= float(comparison)


def conditional_greater_than_or_equal_to(cell_value, comparison):
    """Returns true if the cell value is greater than or equal to
       the comparison, false otherwise"""
    return float(cell_value) >= float(comparison)


def empty(cell_value):
    """Returns true if the cell values is null, false otherwise"""
    return pd.isnull(cell_value)


def occupied(cell_value):
    """Returns true if the cell value is not null, false otherwise"""
    return not pd.isnull(cell_value)


def fill_from_dictionary(mapping, key, transform, df, index, dicts):
    """Fills in object values from a dictionary file"""
    dict_key = transform['key']
    if isinstance(dict_key, dict):
        source_col = transform['key']['sourceCol']
        dict_key = df[source_col][index]
    name = transform['dictionaryName']
    fill_value = (dicts[name][dict_key]
                  if name in dicts and dict_key in dicts[name] else None)
    del mapping[key]['transforms']
    mapping[key] = fill_value


available_comparison_values = {
    'empty': empty,
    'occupied': occupied
}

available_conditionals = {
    'eq': conditional_equal,
    'less-than': conditional_less_than,
    'greater-than': conditional_greater_than,
    'less-than-or-equal-to': conditional_less_than_or_equal_to,
    'greater-than-or-equal-to': conditional_greater_than_or_equal_to,
    'not-eq': (lambda x, y: not conditional_equal(x, y)),
    'not-less-than': (lambda x, y: not conditional_less_than(x, y)),
    'not-greater-than': (lambda x, y: not conditional_greater_than(x, y)),
    'not-less-than-or-equal-to': (lambda x, y:
                                  not conditional_less_than_or_equal_to(x, y)),
    'not-greater-than-or-equal-to': (lambda x, y:
                                     not conditional_greater_than_or_equal_to
                                     (x, y))
}
