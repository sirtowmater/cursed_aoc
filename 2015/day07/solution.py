def try_to_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

def try_and(bits):
    try:
        return bits[0] & bits[1]
    except TypeError:
        return 
def try_not(bits):
    try:
        return bits[0] & bits[1]
    except TypeError:
        return 
def try_or(bits):
    try:
        return bits[0] & bits[1]
    except TypeError:
        return 
def try_lshift(bits):
    try:
        return bits[0] & bits[1]
    except TypeError:
        return 
def try_rshift(bits):
    try:
        return bits[0] & bits[1]
    except TypeError:
        return

def try_in_signal(signal, bit):
    try:
        value = signal[bit]
        return True
    except KeyError:
        return False

def main():
    with open("input.txt", "r") as file:
        content = file.read()
    signal = {}
    solvable_list, not_yet_list = seperate_solvable(content)
    while not_yet_list:
        signal = solver(signal, solvable_list)
        not_yet_list = updater(signal, not_yet_list)
        solvable_list, not_yet_list = seperate_solvable2(solvable_list, not_yet_list)
        print(solvable_list)
        print(signal)
        print(len(not_yet_list))
    print(solvable_list)
    print(signal)
    print(not_yet_list)
    print(signal['lx'])

def seperate_solvable(content):
    solvable_list = []
    not_yet_list = []
    gates = [' AND ', 'NOT ', ' OR ', ' LSHIFT ', ' RSHIFT ']

    for line in content.splitlines():
        breakdown = line.split(' -> ')
        
        solvable = True
        for gate in gates:
            if gate in breakdown[0]:
                bit_operation = breakdown[0].split(gate)
                if gate != 'NOT ':
                    solvable = try_to_int(bit_operation[0]) and try_to_int(bit_operation[1])
                else:
                    solvable = try_to_int(bit_operation[1])
                if solvable:
                    solvable_list.append(line)
                    break

        if solvable:
            if try_to_int(breakdown[0]):
                solvable_list.append(line)
                continue
        else:
            not_yet_list.append(line)

    return solvable_list, not_yet_list

def seperate_solvable2(solvable_list, not_yet_list):
    gates = [' AND ', 'NOT ', ' OR ', ' LSHIFT ', ' RSHIFT ']
    new_not_yet_list = []
    print(len(solvable_list))
    print(len(not_yet_list))
    for line in not_yet_list:
        breakdown = line.split(' -> ')
        
        solvable = True
        for gate in gates:
            if gate in breakdown[0]:
                bit_operation = breakdown[0].split(gate)
                if gate != 'NOT ':
                    solvable = try_to_int(bit_operation[0]) and try_to_int(bit_operation[1])
                else:
                    solvable = try_to_int(bit_operation[1])
                if solvable:
                    # print(breakdown)
                    solvable_list.append(line)
                    break

        if solvable:
            if try_to_int(breakdown[0]):
                solvable_list.append(line)
                continue
        else:
            
            new_not_yet_list.append(line)
    return solvable_list, new_not_yet_list

def solver(signal, solvable_list):
    for line in solvable_list:
        breakdown = line.split(' -> ')
        
        gates = [' AND ', 'NOT ', ' OR ', ' LSHIFT ', ' RSHIFT ']
        for gate in gates:
            if gate in breakdown[0]:
                bit_operation = breakdown[0].split(gate)
                if gate != 'NOT ':
                    bit_operation[0] = (int(bit_operation[0]) if try_to_int(bit_operation[0]) else bit_operation[0])
                bit_operation[1] = (int(bit_operation[1]) if try_to_int(bit_operation[1]) else bit_operation[1])
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
    return signal

def updater(signal, not_yet_list):
    updated_list = []
    for line in not_yet_list:
        breakdown = line.split(' -> ')
        gates = [' AND ', 'NOT ', ' OR ', ' LSHIFT ', ' RSHIFT ']
        for gate in gates:
            if gate in breakdown[0]:
                bit_operation = breakdown[0].split(gate)
                bit_operation[0] = (signal[bit_operation[0]] if try_in_signal(signal, bit_operation[0]) else bit_operation[0])
                bit_operation[1] = (signal[bit_operation[1]] if try_in_signal(signal, bit_operation[1]) else bit_operation[1])
                match gate:
                    case ' AND ':
                        new_line = f'{bit_operation[0]} AND {bit_operation[1]} -> {breakdown[1]}'
                    case 'NOT ':
                        new_line = f'NOT {bit_operation[1]} -> {breakdown[1]}'
                    case ' OR ':
                        new_line = f'{bit_operation[0]} OR {bit_operation[1]} -> {breakdown[1]}'
                    case ' LSHIFT ':
                        new_line = f'{bit_operation[0]} LSHIFT {bit_operation[1]} -> {breakdown[1]}'
                    case ' RSHIFT ':
                        new_line = f'{bit_operation[0]} RSHIFT {bit_operation[1]} -> {breakdown[1]}'
                updated_list.append(new_line)
                break
    return updated_list

if __name__ == "__main__":
    main()