import unittest
from shared.main import load_data


class TestLoadData(unittest.TestCase):

    def test_load_data_to_multidimensional_list(self):
        assert type(load_data('test_input.txt')) == list
