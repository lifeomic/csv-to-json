"""Accepts input csv and mapping file and outputs JSON lines file"""

import argparse
import json
import pandas as pd

from transforms.file_transforms import perform_file_transforms
from transforms.column_transforms import perform_column_transforms
from transforms.generation_transforms import perform_generation_transforms

parser = argparse.ArgumentParser(
    description='Convert .csv file to .json based on supplied mappings file')
parser.add_argument('-i', metavar='Input File', dest='input_file',
                    required=True, help='The input .csv file')
parser.add_argument('-m', metavar='Map File', dest='map_file',
                    required=True,
                    help='The .json file to map the .csv file to')
parser.add_argument('-o', metavar='Output File', dest='output_file',
                    required=True, help='The output .json file')
parser.add_argument('-s', metavar='Input File Separation',
                    dest='separation', required=False,
                    help='The character that separates values in the csv',
                    default=',')
parser.add_argument('-ocsv', metavar='Output CSV File', dest='output_csv',
                    required=False,
                    help='Optional field output the modified csv file if \
                    more transformations are required on top of it',
                    default=None)

if __name__ == '__main__':

    args = parser.parse_args()
    input_file = args.input_file
    map_file = args.map_file
    output_file = args.output_file
    output_csv = args.output_csv
    separation = args.separation
    input_df = pd.read_csv(input_file, dtype='str', sep=separation)
    with open(map_file, 'r') as mp:
        mappings = json.load(mp)
    file_dictionaries = {}
    mappings, input_df, file_dictionaries = perform_file_transforms(
        mappings, input_df, file_dictionaries)
    mappings, input_df = perform_column_transforms(mappings, input_df)
    input_df = perform_generation_transforms(
        mappings, input_df, output_file, file_dictionaries)
    if output_csv:
        input_df.to_csv(output_csv)
