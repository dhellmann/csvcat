import unittest

from csvcat import main


class ColumnNumParseTest(unittest.TestCase):

    def test_single_num(self):
        cols = main._get_column_nums_from_args(['1'])
        self.assertEqual([0], cols)

    def test_not_num(self):
        self.assertRaises(ValueError,
                          main._get_column_nums_from_args,
                          ['a'])

    def test_two_values_with_comma(self):
        cols = main._get_column_nums_from_args(['1,2'])
        self.assertEqual([0, 1], cols)

    def test_spaces_and_commas(self):
        cols = main._get_column_nums_from_args(['1, 2'])
        self.assertEqual([0, 1], cols)

    def test_two_values_with_hyphen(self):
        cols = main._get_column_nums_from_args(['1-3'])
        self.assertEqual([0, 1, 2], cols)

    def test_reverse_range(self):
        cols = main._get_column_nums_from_args(['3-1'])
        self.assertEqual([2, 1, 0], cols)

    def test_combination(self):
        cols = main._get_column_nums_from_args(['1', '5-3', '6,7', '9-11'])
        self.assertEqual([0, 4, 3, 2, 5, 6, 8, 9, 10], cols)
