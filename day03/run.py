from input import paths, paths2, paths3, paths4

paths = [p.split(',') for p in paths]
paths = [[(item[:1], int(item[1:])) for item in path] for path in paths]

def dist(a, b):
    ax, ay = a
    bx, by = b
    return abs(ax - bx) + abs(ay - by)

def find_min_dist(it, dist):
    found_dist = 99999999999999999999
    p0 = 0, 0
    for p in it:
        if p == p0:
            continue
        p_dist = dist(p)
        if p_dist < found_dist and p_dist != (0, 0):
            print(p, p_dist)
            found_dist = p_dist
    return found_dist


def trace(path):
    px, py = 0, 0
    dist = 0
    points = {(px, py): 0}
    add = lambda p, dist: points.setdefault(p, dist)
    print('---')
    for (dir, v) in path:
        print(dir, v, (px, py))
        if dir == 'U':
            for y in range(py + 1, py + v + 1):
                dist += 1
                add((px, y), dist)
            py = py + v
        elif dir == 'D':
            for y in reversed(range(py - v, py)):
                dist += 1
                add((px, y), dist)
            py = py - v
        elif dir == 'R':
            for x in range(px + 1, px + v + 1):
                dist += 1
                add((x, py), dist)
            px = px + v
        elif dir == 'L':
            for x in reversed(range(px - v, px)):
                dist += 1
                add((x, py), dist)
            px = px - v
        else:
            assert False
    return points

a = trace(paths[0])
b = trace(paths[1])

# print(paths[0])
# print(paths[1])
print(a)
print(b)
dist = lambda p: a[p] + b[p]
print(set(a.keys()) & set(b.keys()))
print(find_min_dist(set(a.keys()) & set(b.keys()), dist))
