test_input = [
    0, 3, 6, 9, 12, 15,
    1, 3, 6, 10, 15, 21,
    10, 13, 16, 21, 30, 45,
]

not_consecutive_differ_row = [1, 3, 6, 10, 15, 21]


def get_next_row(row: list) -> list:
    """
        Return next row with one element less len(row) - 6 return 5
    """
    new_row = []

    for i, element in enumerate(row):
        if i + 1 == len(row):
            return new_row

        print(row[i + 1] - row[i])

        new_row.append(row[i + 1] - row[i])


assert [2, 3, 4, 5, 6] == get_next_row(not_consecutive_differ_row)
assert [0, 0] == get_next_row([1, 1, 1])
