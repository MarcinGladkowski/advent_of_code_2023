class Race:
    def __init__(self, time: int, distance: int):
        self.distance = distance
        self.time = time


def is_win_for_hold(hold: int, race: Race) -> bool:
    time_to_ride = race.time - hold
    ride_distance = hold * time_to_ride

    return ride_distance > race.distance


assert False == is_win_for_hold(1, Race(7, 9))
assert is_win_for_hold(2, Race(7, 9))
assert is_win_for_hold(3, Race(7, 9))
assert is_win_for_hold(4, Race(7, 9))
assert is_win_for_hold(5, Race(7, 9))
assert False == is_win_for_hold(6, Race(7, 9))
assert False == is_win_for_hold(7, Race(7, 9))
