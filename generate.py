import time
from random import random
from utils import pr

MaxIter = 10 ** 4
NumPoints = 10 ** 7


def iterate(c):
    z = 0
    l = []
    for i in range(MaxIter):
        if abs(z) > 2:
            return l
        l += [(z, i)]
        z = z ** 2 + c #  Buddhabrot
        # z = z ** 2 - z + c #  Lotus
        # z = 2 * z ** 3 - z ** 2 + z + c #  Butterfly
    return []
    

with open('.data/points.dat', 'a') as f:
    amount = 0

    st = time.time()

    pb = pr.Bar()
    pb.start()

    while amount < NumPoints:
        pb.update(amount / NumPoints)
        re = -2.5 + 5 * random()
        im = -2.5 + 5 * random()
        for (p, i) in iterate(re+im*1j):
            f.write("{} {} {} {} {}\n".format(re, im, p.real, p.imag, i))
            amount += 1
    pb.end()
    print("Finished after {:.2f} seconds".format(time.time() - st))
