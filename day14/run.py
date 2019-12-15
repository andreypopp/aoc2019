import collections
import pprint
from decimal import Decimal

class res(collections.namedtuple('res', 'v unit')):
    def __repr__(self):
        return '%i %s' % (self.v, self.unit)

def parse_res(v):
    v, unit = v.split(' ')
    v = int(v)
    return res(v, unit.upper())

def parse(sch):
    by_unit = {}
    sch = sch.strip()
    for line in sch.split('\n'):
        inp, out = line.split('=>')
        inp = [parse_res(x.strip()) for x in inp.split(',')]
        out = parse_res(out.strip())
        by_unit[out.unit] = (inp, out)
    return by_unit


def run(sch, m=1, ore=None, store=None, trace=False):
    queue = [res(m, 'FUEL')]
    store = store or {}
    ore = None or 0
    while queue:
        if trace:
            print '-----'
            print 'QUEUE %r' % queue
        req = queue.pop(0)
        if trace:
            print 'REQ   %i %s' % (req.v, req.unit)
        exists = store.get(req.unit, 0)
        if req.unit == 'ORE':
            ore = ore + req.v
            continue
        if exists >= req.v:
            v = exists - req.v
            store[req.unit] = v
            continue

        inps, out = sch[req.unit]
        assert out.unit == req.unit

        x = 1
        while (exists + out.v * x) < req.v:
            x = x + 1
        if trace:
            print 'BUILD %i %s' % (x * out.v, req.unit)
            print 'STORE %r' % store
        v = exists + x * out.v - req.v
        store[req.unit] = v
        queue = [r._replace(v=r.v * x) for r in inps] + queue

    return store, ore


def reduce(sch):
    ore = Decimal(0)
    queue = [res(Decimal(1), 'FUEL')]
    while queue:
        req = queue.pop(0)
        if req.unit == 'ORE':
            ore = ore + req.v
            continue
        inps, out = sch[req.unit]
        assert out.unit == req.unit
        k = Decimal(req.v) / Decimal(out.v)
        queue = [r._replace(v=Decimal(r.v) * k) for r in inps] + queue
    return ore



ex1 = parse("""
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
""")

ex2 = parse("""
9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL
""")

ex3 = parse("""
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
""")

ex4 = parse("""
2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF
""")

ex5 = parse("""
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
""")

cargo = Decimal(1000000000000)

def solve(name, sch):
    store, ore = run(sch)
    ore = Decimal(ore)
    print '--- %s' % name
    print '  ORE/CYCLE:          %s' % ore
    print '  FUEL/CARGO:         %s' % (cargo / ore)
    ore_ex = reduce(sch)
    print '  ORE/CYCLE (EXACT):  %s' % ore_ex
    print '  FUEL/CARGO (EXACT): %s' % (cargo / ore_ex - (ore - ore_ex) / ore_ex)

solve('ex1', ex1)
solve('ex2', ex2)
solve('ex3', ex3)
solve('ex4', ex4)
solve('ex5', ex5)

from input import inp

sch = parse(inp)

solve('OUT', sch)
