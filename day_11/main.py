from shared.main import load_data

test_galaxy_raw = load_data('test_input.txt')


def parse(raw: list) -> list:
    data = []
    for row in raw:
        data.append([x for x in row])
    return data


test_galaxy = parse(test_galaxy_raw)
