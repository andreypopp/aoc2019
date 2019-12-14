# encoding: utf-8

import collections

class Out(object):
    def __init__(self, v):
        self.v = v

class Inp(object):
    def __init__(self):
        pass

class Stop(object):
    def __init__(self):
        pass

mode_name = {1: 'imm', 0: 'pos', 2: 'rel'}

def intcode(code, trace=False):
    if trace:
        print('-----------')

    idx = 0
    base = 0
    while True:
        if trace:
            print('--- IDX %i ---' % idx)
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
                print('  GET(%s) %i = %i' % (mode_name[mode], idx + n, v))
            return v

        def set(n, v):
            mode = modes[n - 1]
            if trace:
                print('  SET(%s) %i = %i' % (mode_name[mode], idx + n, v))
            if mode == 0:
                code[code[idx + n]] = v
            elif mode == 1:
                code[idx + n] = v
            elif mode == 2:
                code[base + code[idx + n]] = v
            else:
                raise Exception("invalid mode", mode)

        if opcode == 99:
            if trace:
                print('EXIT')
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
            a1 = get(1)
            a2 = get(2)
            if trace:
                print('JUMP-IF-TRUE %r' % (a1,))
            # 369 is the condition which checks failure, which just say it never
            # happen!
            if idx == 369:
                print('NOT GONNA LOOSE!!!')
                idx = a2
                continue
            if a1 != 0:
                v = a2
                if trace:
                    print('JUMP %i' % v)
                idx = v
            else:
                idx = idx + 3
        elif opcode == 6:
            if trace:
                print('JUMP-IF-FALSE %r' % (get(1),))
            if get(1) == 0:
                v = get(2)
                if trace:
                    print('JUMP %i' % v)
                idx = v
            else:
                idx = idx + 3
        elif opcode == 7:
            a1 = get(1)
            a2 = get(2)
            if trace:
                print('IF-LE %r < %r' % (a1, a2))
            if a1 < a2:
                set(3, 1)
            else:
                set(3, 0)
            idx = idx + 4
        elif opcode == 8:
            a1 = get(1)
            a2 = get(2)
            if trace:
                print('IF-EQ %r == %r' % (a1, a2))
            if a1 == a2:
                set(3, 1)
            else:
                set(3, 0)
            idx = idx + 4
        elif opcode == 9:
            a1 = get(1)
            if trace:
                print('SET-BASE %r' % a1)
            base = base + get(1)
            idx = idx + 2
        else:
            raise Exception("invalid instruction", opcode)

def init(prg, trace=False):
    mem = collections.defaultdict(lambda: 0, enumerate(prg))
    return intcode(mem, trace=trace)

def run(state):
    v = next(state)
    map = {}
    while True:
        if isinstance(v, Stop):
            break
        elif isinstance(v, Out):
            x = v.v
            v = next(state)
            y = v.v
            v = next(state)
            t = v.v
            if (x, y) == (-1, 0):
                print 'SCORE: ', t
            else:
                assert y >= 0, y
                assert x >= 0, x
                tt = tiles.get(t)
                assert tt, tt
                map[(x, y)] = tt
            v = next(state)
        elif isinstance(v, Inp):
            draw(map)
            inp = 0
            v = state.send(inp)
        else:
            raise Exception("Unknown state %r" % v)


tiles = {
    0: ' ',
    1: '▒',
    2: '▓',
    3: '▂',
    4: 'o',
}


def draw(map):
    for y in range(0, 24):
        line = []
        for x in range(0, 42):
            t = map.get((x, y), ' ')
            line.append(t)
        print(''.join(line))



from input import prg
from pprint import pprint

prg = prg[:]
prg[0] = 2
run(init(prg))
