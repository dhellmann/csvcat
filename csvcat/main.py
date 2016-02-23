#!/usr/bin/env python
"""Concatenate csv files.
"""

from __future__ import print_function

import argparse
import csv
import sys


def _get_column_nums_from_args(columns):
    """Turn column inputs from user into list of simple numbers.

    Inputs can be:

      - individual number: 1
      - range: 1-3
      - comma separated list: 1,2,3,4-6
    """
    nums = []
    for c in columns:
        for p in c.split(','):
            p = p.strip()
            try:
                c = int(p)
                nums.append(c)
            except (TypeError, ValueError):
                start, ignore, end = p.partition('-')
                try:
                    start = int(start)
                    end = int(end)
                except (TypeError, ValueError):
                    raise ValueError(
                        'Did not understand %r, expected digit-digit' % c
                    )
                inc = 1 if start < end else -1
                nums.extend(range(start, end + inc, inc))
    # The user will pass us 1-based indexes, but we need to use
    # 0-based indexing with the row.
    return [n - 1 for n in nums]


def _get_printable_columns(columns, row):
    """Return only the part of the row which should be printed.
    """
    if not columns:
        return row

    # Extract the column values, in the order specified.
    return tuple(row[c] for c in columns)


class HelpAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()
        print("""
To concatenate 2 files, including all columns and headers:

  $ csvcat file1.csv file2.csv

To concatenate 2 files, skipping the headers in the second file:

  $ csvcat --skip-headers file1.csv file2.csv

To concatenate 2 files, including only the first and third columns:

  $ csvcat --col 0,2 file1.csv file2.csv
""")
        sys.exit(0)


def main():
    parser = argparse.ArgumentParser(
        description='Concatenate comma separated value files.',
        add_help=False,
    )
    parser.add_argument(
        '--help', '-h',
        action=HelpAction,
        nargs=0,
        help='show this help message and exit',
    )
    parser.add_argument(
        '--skip-headers',
        help=('treat the first line of each file as a header,'
              'and only include one copy in the output.'),
        action='store_true',
        default=False,
    )
    parser.add_argument(
        '--columns', '--col', '-c',
        help=("limit the output to the specified columns."
              "Columns are identified by number, starting with 0."),
        default=[],
        action='append',
    )
    parser.add_argument(
        '--dialect', '-d',
        help=('specify the output dialect name.'
              'Defaults to %(default)s.'),
        default='excel',
        choices=csv.list_dialects(),
    )
    parser.add_argument(
        'filename',
        nargs='+',
        help='files to process',
    )
    args = parser.parse_args()

    columns = _get_column_nums_from_args(args.columns)
    writer = csv.writer(sys.stdout, dialect=args.dialect)
    headers_written = False

    for filename in args.filename:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            if args.skip_headers:
                if not headers_written:
                    # This row must include the headers for the output
                    headers = next(reader)
                    writer.writerow(_get_printable_columns(columns, headers))
                    headers_written = True
                else:
                    # We have seen headers before, and are skipping,
                    # so do not write the first row of this file.
                    next(reader)

            # Process the rest of the file
            for row in reader:
                writer.writerow(_get_printable_columns(columns, row))


if __name__ == '__main__':
    main()
