

def spans(a):
    dots = sorted(a)
    ranges = []
    p = None
    for i in range(len(dots)-1):
        if i == 0:
            ranges.append([dots[i]])
            p = dots[i]
        else:
            if dots[i+1] - dots[i] >= 10:
                p = dots[i + 1]
                ranges[-1].append(dots[i])
                ranges.append([p])
    ranges[-1].append(dots[-1])
    return ranges

def spans2(a):
    dots = sorted(a)
    deltas = []
    for i in range(len(dots) - 1):
        d = dots[i+1] - dots[i]
        deltas.append(d)

    ranges = []
    seconds = 0

    for x in deltas:
        if x < 10:
            seconds += x
    return seconds

def sum_pair(a):
    s = 0
    for x in a:
        d = x[1] - x[0]
        s += d
    return s
