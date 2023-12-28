from pprint import pprint

from shared.main import load_data

test_universum_raw = load_data('test_input.txt')


def parse(raw: list) -> list:
    data = []
    for row in raw:
        data.append([x for x in row])
    return data


test_galaxy = parse(test_universum_raw)


def has_galaxies(universum_row: list) -> bool:
    return len(set(universum_row)) > 1


def expand_row(universum_row: list, expanders: list, expander_sign: str = '.') -> list:
    for i, expander in enumerate(expanders):
        universum_row.insert(expander + i, expander_sign)

    return universum_row


assert ['.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '.', '.', '.'] == expand_row(
    ['.', '.', '.', '#', '.', '.', '.', '.', '.', '.'], [2, 5, 8])

assert has_galaxies(['.', '.']) == False
assert has_galaxies(['.', '#'])


def expand_horizontally(universum: list) -> list:
    """duplicate elements in rows"""
    by_vertical = {}
    for i, row in enumerate(universum):
        for j, cell in enumerate(row):
            if by_vertical.get(j) is None:
                by_vertical[j] = [cell]
                continue

            by_vertical[j].append(cell)

    columns_to_expand = []
    for key, vertical in by_vertical.items():
        if has_galaxies(vertical) is False:
            columns_to_expand.append(key)
            continue

    for r, row_to_expand in enumerate(universum):
        expand_row(row_to_expand, columns_to_expand)

    return universum


def expand_vertically(universum: list) -> list:
    """duplicate row"""
    rows_to_expand = []
    for i, row in enumerate(universum):
        if has_galaxies(row) is False:
            rows_to_expand.append(i)

    empty_row = ['.' for _ in range(0, len(universum[0]))]

    for i, expand in enumerate(rows_to_expand):
        universum.insert(expand + i, empty_row)

    return universum


def expand_universum(galaxy: list) -> list:
    galaxy = expand_horizontally(galaxy)
    galaxy = expand_vertically(galaxy)
    return galaxy


# pprint(object=parse(load_data('test_input_expanded.txt')), width=100)
# pprint(object=expand_universum(test_galaxy), width=100)

"""Get all galaxies"""
expanded_test_galaxy = expand_universum(test_galaxy)


class Galaxy:
    def __init__(self, name: int, position_y: int, position_x: int):
        self.position_x = position_x
        self.position_y = position_y
        self.name = name


def get_galaxies(universe: list) -> list:
    """Get all galaxies from universe"""
    galaxies = []

    for y, row in enumerate(universe):
        for x, cell in enumerate(row):
            if cell == '#':
                name = len(galaxies) + 1
                galaxies.append(Galaxy(name, y, x))

    return galaxies


assert 9 == len(get_galaxies(expanded_test_galaxy))


class GalaxiesPath:
    def __init__(self, galaxy_1: Galaxy, galaxy_2: Galaxy):
        self.galaxy_1 = galaxy_1
        self.galaxy_2 = galaxy_2

    def __str__(self):
        return f"{self.galaxy_1.name}-{self.galaxy_2.name}"

    def __eq__(self, __value):
        if __value is not None and isinstance(__value, GalaxiesPath) is False:
            raise TypeError('GalaxiesPath can only be')

        return (self.galaxy_1.name == __value.galaxy_1.name and self.galaxy_2.name == __value.galaxy_2.name) or (
                self.galaxy_2.name == __value.galaxy_1.name and self.galaxy_1.name == __value.galaxy_2.name)

    def distance(self) -> int:
        y = self.galaxy_2.position_y - self.galaxy_1.position_y
        x = self.galaxy_2.position_x - self.galaxy_1.position_x

        return abs(x) + abs(y)


assert GalaxiesPath(Galaxy(1, 1, 1), Galaxy(2, 2, 2)) == GalaxiesPath(Galaxy(1, 1, 1), Galaxy(2, 2, 2))
assert False == (GalaxiesPath(Galaxy(1, 1, 1), Galaxy(2, 2, 2)) == GalaxiesPath(Galaxy(2, 1, 1), Galaxy(2, 2, 2)))

assert (GalaxiesPath(Galaxy(2, 2, 2), Galaxy(1, 1, 1))
        == GalaxiesPath(Galaxy(1, 1, 1), Galaxy(2, 2, 2)))

assert 15 == GalaxiesPath(Galaxy(1, 0, 4), Galaxy(7, 10, 9)).distance()
assert 17 == GalaxiesPath(Galaxy(3, 2, 0), Galaxy(6, 7, 12)).distance()


def has_path(candidate: GalaxiesPath, paths_combinations: list):
    for path in paths_combinations:
        if candidate == path:
            return True
    return False


def path_combinations(galaxies: list) -> list:
    """
        Unique combinations, not with both the same,
        using index/name to find combinations
    """
    paths_combinations = []

    for idx, galaxy in enumerate(galaxies):
        for next_galaxy_index in range(0, len(galaxies)):

            next_galaxy = galaxies[next_galaxy_index]

            if galaxy == next_galaxy:
                continue

            path_candidate = GalaxiesPath(galaxy, next_galaxy)

            if has_path(path_candidate, paths_combinations):
                continue

            paths_combinations.append(path_candidate)

    return paths_combinations


test_galaxies = get_galaxies(expanded_test_galaxy)

assert 36 == len(path_combinations(test_galaxies))

def calculate_distances(paths: list) -> int:
    return sum(list(map(lambda path: path.distance(), paths)))


assert 374 == calculate_distances(path_combinations(test_galaxies))
