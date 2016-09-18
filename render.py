from PIL import Image
import math
from utils import pr
import time
import cmath

import sys

datafile = '.data/points.dat'  # if len(sys.argv) == 1 else sys.argv[1]+".drata"
imgfile = 'out/fractal.png'  # if len(sys.argv) == 1 else sys.argv[1]+".png"

W, H = 3840, 2160

S_h = 1
S_w = W / H * S_h

Limits = {"r": 10000, "g": 1000, "b": 100}
channels = ["r", "g", "b"]

img = Image.new("RGB", (W, H))


def translate_xy(z):
    x = (S_w + z.real) / (2 * S_w) * W
    y = (S_h - z.imag) / (2 * S_h) * H
    return math.floor(x), math.floor(y)


def translate_c(x, y):
    re = (2 * x / W - 1) * S_w
    im = (2 * y / H - 1) * -S_h
    return re+im*1j

bData = {
    ch: [[0 for i in range(H)] for j in range(W)] for ch in channels
}

print("reading...")
st = time.time()
with open(datafile, 'r') as f:
    for ln in f:
        [sr, si, dr, di, it] = list(map(float, ln[:-1].split(" ")))
        
        x, y = translate_xy(dr + di * 1j)
        if 0 <= x < W and 0 <= y < H:
            for ch in channels:
                if 15 < it <= Limits[ch]:
                    bData[ch][x][y] += 1
print("Finished after {:.2f} seconds".format(time.time() - st))

print("calculating...")
st = time.time()

brightest = {
    ch: max(max(bData[ch][i] for i in range(W))) for ch in channels
    }

for ch in channels:
    assert brightest[ch] != 0

scl = {ch: 255 / brightest[ch] for ch in channels}
imgdata = []


def sc(c):
    return min(255, max(0, math.floor(c+0.5)))


b = pr.Bar()
b.start()

for y in range(H):
    b.update(y / H)
    for x in range(W):
        col = {ch: scl[ch] * bData[ch][x][y] for ch in channels}

        imgdata += [tuple(sc(col[ch]) for ch in channels)]
b.end()
print("Finished after {:.2f} seconds".format(time.time() - st))

print("writing to file...")

img.putdata(imgdata)
img.save(imgfile)

print("done")
