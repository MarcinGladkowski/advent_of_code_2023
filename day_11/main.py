from shared.main import load_data

test_universum_raw = load_data('test_input.txt')


def parse(raw: list) -> list:
    data = []
    for row in raw:
        data.append([x for x in row])
    return data


test_galaxy = parse(test_universum_raw)


def any_galaxies_horizontally(universum_row: list) -> bool:
    return len(set(universum_row)) == 1


assert any_galaxies_horizontally(['.', '.'])
assert any_galaxies_horizontally(['.', '#']) == False


def expand_universum(galaxy: list) -> list:
    """duplicate horizontally row"""
    for row in galaxy:
        pass

    return galaxy


assert expand_universum(test_galaxy) == parse(load_data('test_input_expanded.txt'))
