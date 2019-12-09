import itertools
from input import input
input_ex = '123456789012'

w, h = 3, 2


def parse(it, size):
    seen, acc = 0, []
    for x in it:
        x = int(x)
        if seen == size:
            yield acc
            seen, acc = 0, []
        seen = seen + 1
        acc.append(x)
    assert seen == 0 or seen == size
    if seen == size:
        yield acc


def solve(input, w, h):
    stats_by_layer = []
    for layer in parse(input, w * h):
        print(layer)
        stats = {}
        for d in layer:
            stats[d] = stats.get(d, 0) + 1
        print(stats)
        stats_by_layer.append(stats)

    solution = sorted(stats_by_layer, key=lambda s: s.get(0, 0))[0]
    print(solution)
    print(solution.get(1, 0) * solution.get(2, 0))


def to_img(input, w, h):
    layers = parse(input, w * h)
    img = [2 for _ in range(0, w * h)]
    for layer in reversed(list(layers)):
        for idx, d in enumerate(layer):
            if d != 2:
                img[idx] = d
    assert 2 not in img
    return img

def show_img(img, w, h):
    for line in parse(img, w):
        line = ''.join('*' if d else ' ' for d in line)
        print(line)


show_img(to_img(input, 25, 6), 25, 6)
