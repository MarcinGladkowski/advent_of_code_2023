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
        universum.insert(expand+i, empty_row)

    return universum


def expand_universum(galaxy: list) -> list:
    galaxy = expand_horizontally(galaxy)
    galaxy = expand_vertically(galaxy)
    return galaxy


pprint(object=parse(load_data('test_input_expanded.txt')), width=100)
pprint(object=expand_universum(test_galaxy), width=100)
