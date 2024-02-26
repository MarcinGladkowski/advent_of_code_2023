from main import calculate_hash, get_result, calculate_from_instruction

test_input = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'

generator = calculate_hash('HASH')

assert 200 == next(generator)
assert 153 == next(generator)
assert 172 == next(generator)
assert 52 == next(generator)

assert 52 == get_result('HASH')

### test input
assert 30 == get_result('rn=1')

assert 1320 == calculate_from_instruction(test_input)