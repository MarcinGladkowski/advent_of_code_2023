import unittest

from shared.main import load_data
from main import Point, normalize_data, Dot, MapWalker, Direction
import inspect

TEST_DATA_FILE_NAME = 'test_input.txt'


class TestLoadData(unittest.TestCase):

    def test_load_data_to_multidimensional_list(self):
        assert isinstance(load_data('test_input.txt'), list)

    def test_parse_single_row_data_to_map(self):
        assert len(normalize_data([['.', '.', '.']])[0]) == 3

    def test_storing_unique_points(self):
        assert 2 == len({Dot(0, 0, ''), Dot(0, 0, ''), Dot(0, 1, '')})

    # def test_load_add_elements_normalized_to_type_point(self):
    #
    #     data = load_data(TEST_DATA_FILE_NAME)
    #
    #     normalized = normalize_data(data)
    #
    #     for row in normalized:
    #         for element in row:
    #             assert element.y is not None
    #             assert element.x is not None
    #             assert element.sign is not None

    def test_continue_path_from_dot_to_dot(self):

        input_one_row_map = normalize_data([['.', '.', '.']])
        walker = MapWalker(input_one_row_map, Dot(0, 0, '.'))
        walker.next()

        assert walker._cursor.x == 1
        assert walker._cursor.y == 0

    def test_return_next_element_from_map_by_direction(self):
        input_one_row_map = normalize_data([['.', '.', '.']])
        walker = MapWalker(input_one_row_map, Dot(0, 0, '.'))

        assert Dot(0, 1, '.') == walker.get_next_point(Direction.RIGHT)


    def test_store_three_points_moving_right(self):

        input_one_row_map = normalize_data([['.', '.', '.']])
        walker = MapWalker(input_one_row_map, Dot(0, 0, '.'))

        walker.next()
        walker.next()

        assert 3 == len(walker._visited)

        # input_one_row_map = normalize_data([
        #     ['.', '.', '.'],
        #     ['.', '|', '.'], # start of left side
        #     ['.', '.', '.'],
        # ])
        #
        # walker = MapWalker(input_one_row_map, Dot(1, 0, '.'))
        #
        # walker.next()


