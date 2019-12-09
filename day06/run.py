input = '''
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
'''

input2 = '''
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN
'''

def parse(input):
    orbits = {}
    for line in input.strip().split('\n'):
        x, y = line.split(')')
        orbits[y] = x
    return orbits


def transitive_closure(rels):
    closure = set()
    queue = list(rels.items())
    while queue:
        k, v = queue.pop()
        closure.add((k, v))
        vv = rels.get(v)
        if vv is None or (k, vv) in closure:
            continue
        queue.append((k, vv))
    return closure


def trace(rels, a, b):
    jumps = {}
    for k, v in rels.items():
        jumps[k] = {v}
    for k, v in rels.items():
        e = jumps.get(v, set())
        e.add(k)
        jumps[v] = e

    queue = [(a, [])]
    res = []
    while queue:
        p, trace = queue.pop()
        if p == b:
            trace = trace + [p]
            res.append(trace)
            continue
        next = jumps.get(p, set()) - set(trace)
        for next_p in next:
            next_trace = trace + [p]
            queue.append((next_p, next_trace))
    return res



from input import input as real_input
from pprint import pprint

rels = parse(real_input)
pprint(rels)
A = rels['YOU']
B = rels['SAN']
traces = trace(rels, A, B)
pprint(len(traces[0]) - 1)
