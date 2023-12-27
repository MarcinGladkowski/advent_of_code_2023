from shared.main import load_data
from main import parse_data

data_part_1 = load_data('input.txt')
points = load_data('path.txt')

data = parse_data(data_part_1)

print(data)

for point in points:
    y, x = point.split(';')
    data[int(y)][int(x)] = '#'



f = open("input_with_map.txt", "w")

for row in data:
    f.write(''.join(row)+"\n")

