start = 307237
stop = 769058

def to_num(a, b, c, d, e, f):
    return a * 100000 + b * 10000 + c * 1000 + d * 100 + e * 10 + f

def of_num(n):
    return (n / 100000, n / 10000, n / 1000, n / 100, n / 10, n)

def gen(start, stop):
    found = 0
    for a in range(1, 10):
        for b in range(a, 10):
            for c in range(b, 10):
                for d in range(c, 10):
                    for e in range(d, 10):
                        for f in range(e, 10):
                            if a == b and b != c \
                            or b == c and a != b and c != d \
                            or c == d and b != c and d != e \
                            or d == e and c != d and e != f \
                            or e == f and d != e:
                                n = to_num(a, b, c, d, e, f)
                                if start <= n <= stop:
                                    print(n)
                                    found = found + 1
    print(found)


gen(start, stop)
