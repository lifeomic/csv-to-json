import pandas as pd


def deletion_conditional(mapping, key, conditional, df, index):
    if (not handle_conditional(conditional, df, index) and
            (isinstance(mapping, list) or (isinstance(mapping, dict) and
                                           key in mapping))):
        del mapping[key]


def conditional(mapping, key, conditional, df, index):
    if handle_conditional(conditional, df, index):
        handle_conditional_value(
            mapping, key, conditional, df, index, 'true')
    else:
        handle_conditional_value(
            mapping, key, conditional, df, index, 'false')


def handle_conditional(conditional, df, index):
    if ('condition' in conditional and
            conditional['condition'] in available_conditionals):
        condition_function = available_conditionals[conditional['condition']]
        cell_value = df[conditional['sourceCol']][index]
        comparison = conditional['compareTo']
        return condition_function(cell_value, comparison)


def handle_conditional_value(mapping, key, conditional, value):
    if key not in mapping:
        return
    if (isinstance(conditional['values'][value], dict) and
            'sourceCol' in conditional['values'][value]):
        mapping['sourceCol'] = conditional['values'][value]['sourceCol']
    else:
        string_value = conditional['values'][value]
        del mapping[key]['transforms']
        mapping[key] = string_value


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
