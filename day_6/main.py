from shared.main import load_data

test_data = load_data('input_test.txt')


class Race:
    def __init__(self, time: int, distance: int):
        self.distance = distance
        self.time = time


def parse_data(data: list) -> tuple:
    for line in data:
        if line.startswith('Time'):
            title, race_times = line.split(':')

    for line in data:
        if line.startswith('Time'):
            title, distances = line.split(':')

    return race_times, distances


def parse_lists(raw_data: str):
    return list(map(lambda x: int(x), filter(lambda x: x.isnumeric(), raw_data)))


times, distances = parse_data(test_data)
times = parse_lists(times)

distances = parse_lists(distances)


def to_races(times: list, distances: list) -> list:
    races = []
    for i in range(len(times)):
        races.append(Race(times[i], distances[i]))

    return races


print(to_races(times, distances))


class RaceWinCalculator:

    @staticmethod
    def count_win_holds(race: Race):
        count = 0
        for time_hold in range(race.time + 1):
            if RaceWinCalculator.is_win_for_hold(time_hold, race):
                count += 1

        return count

    @staticmethod
    def is_win_for_hold(hold: int, race: Race) -> bool:
        time_to_ride = race.time - hold
        ride_distance = hold * time_to_ride

        return ride_distance > race.distance


assert False == RaceWinCalculator.is_win_for_hold(1, Race(7, 9))
assert RaceWinCalculator.is_win_for_hold(2, Race(7, 9))
assert RaceWinCalculator.is_win_for_hold(3, Race(7, 9))
assert RaceWinCalculator.is_win_for_hold(4, Race(7, 9))
assert RaceWinCalculator.is_win_for_hold(5, Race(7, 9))
assert False == RaceWinCalculator.is_win_for_hold(6, Race(7, 9))
assert False == RaceWinCalculator.is_win_for_hold(7, Race(7, 9))

assert 4 == RaceWinCalculator.count_win_holds(Race(7, 9))
assert 8 == RaceWinCalculator.count_win_holds(Race(15, 40))
assert 9 == RaceWinCalculator.count_win_holds(Race(30, 200))
