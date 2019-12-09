import time

def intcode(code, trace=False):
    if trace:
        print('-----------')
    code = code[:]

    idx = 0
    while True:
        if trace:
            print('idx', idx)
            print('code', code)
        instr = code[idx]
        mode3 = instr / 10000
        mode2 = instr / 1000 - mode3 * 10
        mode1 = instr / 100 - mode3 * 100 - mode2 * 10
        modes = [mode1, mode2, mode3]
        opcode = instr - mode1 * 100 - mode2 * 1000 - mode3 * 10000

        def get(n):
            mode = modes[n - 1]
            if mode == 0:
                v = code[code[idx + n]]
            elif mode == 1:
                v = code[idx + n]
            else:
                raise Exception("invalid mode", mode)
            if trace:
                print('get %s %i = %i' % ('imm' if mode else 'pos', idx + n, v))
            return v

        def set(n, v):
            mode = modes[n - 1]
            if trace:
                print('set', 'imm' if mode else 'pos', n, idx + n, v)
            if mode == 0:
                code[code[idx + n]] = v
            elif mode == 1:
                code[idx + n] = v
            else:
                raise Exception("invalid mode", mode)

        if trace:
            print(opcode, mode1, mode2, mode3)
        if opcode == 99:
            break
        elif opcode == 1:
            a = get(1)
            b = get(2)
            c = a + b
            if trace:
                print("%i + %i = %i" % (a, b, c))
            set(3, c)
            idx = idx + 4
        elif opcode == 2:
            a = get(1)
            b = get(2)
            c = a * b
            if trace:
                print("%i * %i = %i" % (a, b, c))
            set(3, c)
            idx = idx + 4
        elif opcode == 3:
            v = input('INP ')
            set(1, v)
            idx = idx + 2
        elif opcode == 4:
            print('OUT %i' % get(1))
            idx = idx + 2
        elif opcode == 5:
            if get(1) != 0:
                v = get(2)
                if trace:
                    print('JUMP %i' % v)
                idx = v
            else:
                idx = idx + 3
        elif opcode == 6:
            if get(1) == 0:
                v = get(2)
                if trace:
                    print('JUMP %i' % v)
                idx = v
            else:
                idx = idx + 3
        elif opcode == 7:
            if get(1) < get(2):
                set(3, 1)
            else:
                set(3, 0)
            idx = idx + 4
        elif opcode == 8:
            if get(1) == get(2):
                set(3, 1)
            else:
                set(3, 0)
            idx = idx + 4
        else:
            raise Exception("invalid instruction", opcode)



# intcode([1002,4,3,4,33])
# intcode([3,0,4,0,99])


# intcode([3,9,8,9,10,9,4,9,99,-1,8])
# intcode([3,9,7,9,10,9,4,9,99,-1,8])
# intcode([3,3,1108,-1,8,3,4,3,99])
# intcode([3,3,1107,-1,8,3,4,3,99])

# intcode([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9])

from code import code
intcode(code)
