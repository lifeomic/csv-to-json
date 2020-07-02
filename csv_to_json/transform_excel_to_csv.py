"""Utility function to transform an excel file to csv or tsv file"""

import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Convert .xlsx file to .csv file')
parser.add_argument('-i', metavar='Input File', dest='input_file',
                    required=True, help='The input .xlsx file')
parser.add_argument('-s', metavar='Sheet', dest='sheet', required=False,
                    help='The desired sheet in the .xlsx file', default='0')
parser.add_argument('-o', metavar='Output File', dest='output_file',
                    required=True, help='The output .csv file')

if __name__ == '__main__':

    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file
    sheet_name = args.sheet

    xls = pd.read_excel(input_file, sheet_name, index_col=None)
    xls.to_csv(output_file, encoding='utf-8', sep=',', index=False)
