
class Out(object):
    def __init__(self, v):
        self.v = v

class Inp(object):
    def __init__(self):
        pass

class Stop(object):
    def __init__(self):
        pass

def intcode(code, trace=False):
    if trace:
        print('-----------')

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
        else:
            raise Exception("invalid instruction", opcode)

from code import code
code_ex = [
    3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
    27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
]

def run_one(item, out):
    (name, agent, state) = item
    if isinstance(state, Inp):
        state = agent.send(out)
        return run_one((name, agent, state), out)
    elif isinstance(state, Out):
        return (name, agent, next(agent)), state.v
    elif isinstance(state, Stop):
        return None, out

def init_scheduler(code, phases):
    phases = iter(phases)
    queue = []
    for name in 'ABCDE':
        agent = intcode(code[:])
        n = next(agent)
        assert isinstance(n, Inp)
        state = agent.send(next(phases))
        queue.append((name, agent, state))
    return queue

def run_scheduler(queue):
    out = 0

    while queue:
        item = queue.pop(0)
        item, out = run_one(item, out)
        if item is not None:
            queue.append(item)

    return out

import itertools

print(max(
    run_scheduler(init_scheduler(code, phases))
    for phases
    in itertools.permutations([5, 6, 7, 8, 9], 5)
))
