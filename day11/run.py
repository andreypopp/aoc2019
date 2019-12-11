from collections import defaultdict
from input import prg

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




def init(prg, trace=False):
    return intcode(Memory(prg), trace=trace)


def step(state, value, expect=None):
    v = state.send(value)
    if expect is not None:
        assert isinstance(v, expect)
    return v


LEFT = 0
RIGHT = 1
BLACK = 0
WHITE = 1

to_left = {
    'u': 'l',
    'r': 'u',
    'd': 'r',
    'l': 'd',
}

to_right = {
    'u': 'r',
    'r': 'd',
    'd': 'l',
    'l': 'u',
}

to_incr = {
    'u': lambda (x, y): (x, y + 1),
    'r': lambda (x, y): (x + 1, y),
    'd': lambda (x, y): (x, y - 1),
    'l': lambda (x, y): (x - 1, y),
}

def run(state):
    painted = set()
    dir = 'u'
    pos = 0, 0
    board = defaultdict(lambda: BLACK, {pos: WHITE})
    while True:
        v = step(state, None, expect=(Stop, Inp))
        if isinstance(v, Stop):
            break
        inp = board[pos]

        v = step(state, inp, expect=Out)
        assert v.v in (WHITE, BLACK)
        board[pos] = v.v
        painted.add(pos)

        v = step(state, None, expect=Out)
        assert v.v in (LEFT, RIGHT)
        if v.v == LEFT:
            dir = to_left[dir]
        elif v.v == RIGHT:
            dir = to_right[dir]
        else:
            assert 'Unknown direction', dir
        pos = to_incr[dir](pos)

    print('Seen at least once', len(painted))
    return board


def show(board):
    xs = [x for x, y in board.keys()]
    ys = [y for x, y in board.keys()]

    min_x = min(xs)
    max_x = max(xs)

    min_y = min(ys)
    max_y = max(ys)

    print (min_x, max_x)
    print (min_y, max_y)

    for y in range(min_y, max_y + 1):
        line = []
        for x in range(min_x, max_x + 1):
            pos = (x, y)
            c = board[pos]
            if c == BLACK:
                line.append(' ')
            elif c == WHITE:
                line.append('#')
            else:
                assert 'Unknown color', c
        print(''.join(line))


board = run(init(prg))
show(board)
