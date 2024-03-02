import unittest

from shared.main import load_data
from main import Point, normalize_data

TEST_DATA_FILE_NAME = 'test_input.txt'


class TestLoadData(unittest.TestCase):

    def test_load_data_to_multidimensional_list(self):
        assert type(load_data('test_input.txt')) == list

    def test_load_add_elements_normalized_to_type_point(self):

        data = load_data(TEST_DATA_FILE_NAME)

        normalized = normalize_data(data)

        for row in normalized:
            for element in row:
                assert isinstance(element, Point)
