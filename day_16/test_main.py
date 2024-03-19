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

    def test_continue_path_from_dot_to_dot(self):
        input_one_row_map = normalize_data([['.', '.', '.']])
        walker = MapWalker(input_one_row_map, Dot(0, 0, '.'))

        walker.next() # recursion

        assert walker._cursor.x == 2 # last element
        assert walker._cursor.y == 0

    def test_return_next_element_from_map_by_direction(self):
        input_one_row_map = normalize_data([['.', '.', '.']])
        walker = MapWalker(input_one_row_map, Dot(0, 0, '.'))

        assert Dot(0, 1, '.') == walker.get_next_point(Direction.RIGHT)

    def test_return_next_element_right_and_out_of_map(self):
        input_one_row_map = normalize_data([['.']])
        walker = MapWalker(input_one_row_map, Dot(0, 0, '.'))

        assert walker.get_next_point(Direction.RIGHT) is None

    def test_return_next_element_up_and_out_of_map(self):
        input_one_row_map = normalize_data([['.']])
        walker = MapWalker(input_one_row_map, Dot(0, 0, '.'))

        assert walker.get_next_point(Direction.UP) is None

    def test_return_next_element_left_till_edge_of_map(self):
        input_one_row_map = normalize_data([['.']])
        walker = MapWalker(input_one_row_map, Dot(0, 0, '.'), Direction.LEFT)

        walker.next()

        assert walker.get_next_point(Direction.LEFT) is None

    def test_return_next_element_down_till_edge_of_map(self):
        input_one_row_map = normalize_data([['.']])
        walker = MapWalker(input_one_row_map, Dot(0, 0, '.'), Direction.DOWN)

        walker.next()

        assert walker.get_next_point(Direction.DOWN) is None

    def test_store_three_points_moving_right(self):
        input_one_row_map = normalize_data([['.', '.', '.']])
        walker = MapWalker(input_one_row_map, Dot(0, 0, '.'))

        walker.next()

        assert 3 == len(walker._visited)

    def test_split_walker_on_flat_side_of_splitter(self):
        input_one_row_map = normalize_data([
            ['.', '.', '.'],
            ['.', '|', '.'],  # start of left side
            ['.', '.', '.'],
        ])

        walker = MapWalker(input_one_row_map, Dot(1, 0, '.'))
        walker = walker.next()

        assert 2 == len(walker)

    # def test_split_walker_on_flat_side_of_splitter_but_only_split_to_one_path(self):
    #     input_one_row_map = normalize_data([
    #         ['.', '|', '.'],  # start of left side
    #         ['.', '.', '.'],
    #     ])
    #
    #     walker = MapWalker(input_one_row_map, Dot(0, 0, '.'))
    #     walker = walker.next()
    #
    #     assert 1 == len(walker)
