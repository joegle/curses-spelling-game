
def spans2(a):
    "groups score data into sessions and accumulate times"
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

