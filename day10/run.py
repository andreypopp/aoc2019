from pprint import pprint
import math

ex1 = """
.#..#
.....
#####
....#
...##
"""
ex1_expect = ((3, 4), 8)

ex2 = """
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
"""
ex2_expect = ((5, 8), 33)

ex3 = """
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
"""
ex3_expect = ((1, 2), 35)

inp = """
#..#....#...#.#..#.......##.#.####
#......#..#.#..####.....#..#...##.
.##.......#..#.#....#.#..#.#....#.
###..#.....###.#....##.....#...#..
...#.##..#.###.......#....#....###
.####...##...........##..#..#.##..
..#...#.#.#.###....#.#...##.....#.
......#.....#..#...##.#..##.#..###
...###.#....#..##.#.#.#....#...###
..#.###.####..###.#.##..#.##.###..
...##...#.#..##.#............##.##
....#.##.##.##..#......##.........
.#..#.#..#.##......##...#.#.#...##
.##.....#.#.##...#.#.#...#..###...
#.#.#..##......#...#...#.......#..
#.......#..#####.###.#..#..#.#.#..
.#......##......##...#..#..#..###.
#.#...#..#....##.#....#.##.#....#.
....#..#....##..#...##..#..#.#.##.
#.#.#.#.##.#.#..###.......#....###
...#.#..##....###.####.#..#.#..#..
#....##..#...##.#.#.........##.#..
.#....#.#...#.#.........#..#......
...#..###...#...#.#.#...#.#..##.##
.####.##.#..#.#.#.#...#.##......#.
.##....##..#.#.#.......#.....####.
#.##.##....#...#..#.#..###..#.###.
...###.#..#.....#.#.#.#....#....#.
......#...#.........##....#....##.
.....#.....#..#.##.#.###.#..##....
.#.....#.#.....#####.....##..#....
.####.##...#.......####..#....##..
.#.#.......#......#.##..##.#.#..##
......##.....##...##.##...##......
"""


def parse(map):
    lines = map.strip().split('\n')
    hits = set()
    w = len(lines[0])
    h = len(lines)
    for y, line in enumerate(lines):
        for x, loc in enumerate(line):
            if loc == '#':
                hits.add((x, y))
    return hits, (w, h)


def examine(map):
    hits, (w, h) = map
    by_loc = {}
    for x, y in hits:

        info = {}
        for (hx, hy) in hits:
            if (hx, hy) == (x, y):
                continue
            if hx == x:
                gd = 180 if hy > y else 0
            else:
                tg = (float(hy - y) / (hx - x))
                gd = math.atan(tg) * 180 / math.pi
                gd = gd + 90
                if hx < x:
                    gd = gd + 180
            b = hx - x > 0
            c = hy - y > 0
            dist = (hx - x)**2 + (hy - y)**2
            info[gd] = info.get(gd, []) + [((hx, hy), dist)]

        for k in info:
            info[k].sort(key=lambda (p, dist): dist)

        by_loc[(x, y)] = info

    conflicts = lambda info: sum(len(v) - 1 for v in info.values())

    # get by the min number of "conflicts"
    loc = min(by_loc, key=lambda k: conflicts(by_loc[k]))
    info = by_loc[loc]
    num = len(hits) - conflicts(info) - 1

    print('P1', loc, num)

    idx = 0
    while idx <= 200:
        for k in sorted(info.keys()):
            v = info[k]
            if v:
                idx = idx + 1
                if idx == 200:
                    (x, y), d = v.pop(0)
                    print('P2', idx, x * 100 + y)
                else:
                    v.pop(0)


# examine(parse(ex1))
# examine(parse(ex2))
# examine(parse(ex3))
examine(parse(inp))
