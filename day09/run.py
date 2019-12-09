import sys

class Out(object):
    def __init__(self, v):
        self.v = v

class Inp(object):
    def __init__(self):
        pass

class Stop(object):
    def __init__(self):
        pass

class Memory(object):
    def __init__(self, code):
        self.mem = {}
        for idx, v in enumerate(code):
            self.mem[idx] = v

    def __getitem__(self, k):
        assert k >= 0
        return self.mem.get(k, 0)

    def __setitem__(self, k, v):
        assert k >= 0
        self.mem[k] = v

def intcode(code, trace=False):
    if trace:
        print('-----------')

    idx = 0
    base = 0
    while True:
        if trace:
            print('idx', idx)
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
            elif mode == 2:
                v = code[base + code[idx + n]]
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
            elif mode == 2:
                code[base + code[idx + n]] = v
            else:
                raise Exception("invalid mode", mode)

        if trace:
            print('EXEC', opcode, mode1, mode2, mode3)
        if opcode == 99:
            yield Stop()
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
            v = yield Inp()
            if trace:
                print('INP %r' % v)
            set(1, v)
            idx = idx + 2
        elif opcode == 4:
            v = get(1)
            if trace:
                print('OUT %r' % v)
            yield Out(v)
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
        elif opcode == 9:
            base = base + get(1)
            idx = idx + 2
        else:
            raise Exception("invalid instruction", opcode)


def run(state):
    v = next(state)
    while True:
        if isinstance(v, Stop):
            break
        elif isinstance(v, Out):
            print('OUT', v.v)
            v = next(state)
        elif isinstance(v, Inp):
            inp = input()
            print('INP', inp)
            v = state.send(inp)
        else:
            raise Exception("Unknown state %r" % v)


def init(prg, trace=False):
    return intcode(Memory(prg), trace=trace)


ex1 = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
ex2 = [1102,34915192,34915192,7,4,7,99,0]
ex3 = [104,1125899906842624,99]
from input import input as inp
run(init(inp))
