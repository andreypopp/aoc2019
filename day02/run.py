from input import code as orig_code


def run(noun, verb):
    code = orig_code[:]
    code[1] = noun
    code[2] = verb

    idx = 0
    while True:
        instr = code[idx]
        if instr == 99:
            break
        elif instr == 1:
            code[code[idx + 3]] = code[code[idx + 1]] + code[code[idx + 2]]
            idx = idx + 4
        elif instr == 2:
            code[code[idx + 3]] = code[code[idx + 1]] * code[code[idx + 2]]
            idx = idx + 4
        else:
            raise Exception("invalid instruction", instr)

    res = code[0]
    return res

for i in range(0, 100):
    for j in range(0, 100):
        res = run(i, j)
        if res == 19690720:
            print(i, j, i * 100 + j)
            break
