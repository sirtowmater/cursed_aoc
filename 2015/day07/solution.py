def try_to_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


with open("input.txt", "r") as file:
    content = file.read()

signal = {}
for line in content.splitlines():
    breakdown = line.split(' -> ')
    
    gates = [' AND ', 'NOT ', ' OR ', ' LSHIFT ', ' RSHIFT ']
    for gate in gates:
        if gate in breakdown[0]:
            bit_operation = breakdown[0].split(gate)
            if gate != 'NOT ':
                bit_operation[0] = (int(bit_operation[0]) if try_to_int(bit_operation[0]) else signal[bit_operation[0]])
            bit_operation[1] = (int(bit_operation[1]) if try_to_int(bit_operation[1]) else signal[bit_operation[1]])
            match gate:
                case ' AND ':
                    breakdown[0] = bit_operation[0] & bit_operation[1]
                case 'NOT ':
                    breakdown[0] = ~bit_operation[1] & 0xFFFF
                case ' OR ':
                    breakdown[0] = bit_operation[0] | bit_operation[1]
                case ' LSHIFT ':
                    breakdown[0] = bit_operation[0] << bit_operation[1]
                case ' RSHIFT ':
                    breakdown[0] = bit_operation[0] >> bit_operation[1]
            break

    signal[breakdown[-1]] = (int(breakdown[0]) if try_to_int(breakdown[0]) else breakdown[0])

print(signal['a'])