# -*- coding: utf-8 -*-
"""
CLI Interface

@author: Tomas Krizek
"""

from data import parse_format
from data import parse_con
from data import autoconvert
from data import Validator

from argparse import ArgumentParser


def validate(input_=None, format_=None):
    its = parse_format(format_)
    validator = Validator()

    data = parse_con(input_)
    data = autoconvert(data, its)
    validator.validate(data, its)

    print(validator.console_log)

if __name__ == "__main__":
    import os.path
    parser = ArgumentParser(description='Validation of flow123d configuration files.')
    parser.add_argument('input',type=str,
                       help='configuration file to validate (con)')
    parser.add_argument('-f', '--format' , type=str, dest='format',
                       help='format description file (json)')
    args = parser.parse_args()
    if args.input is None or not os.path.isfile(args.input):
        parser.error('Invalid input file.')
    if args.format is None:
        parser.error('No format file specified.')
    if not os.path.isfile(args.format):
        parser.error('Invalid format file.')

    validate(args.input, args.format)
