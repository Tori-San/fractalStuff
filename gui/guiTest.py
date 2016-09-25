import tkinter as tk
from PIL import Image, ImageTk
import math

MAX_ITERATIONS = 200
W, H = 1000, 1000
S_h = 1
S_w = W / H * S_h


def translate_xy(z):
    x = (S_w + z.real) / (2 * S_w) * W
    y = (S_h - z.imag) / (2 * S_h) * H
    return math.floor(x), math.floor(y)


def translate_c(x, y):
    re = (2 * x / W - 1) * S_w
    im = (2 * y / H - 1) * -S_h
    return re+im*1j


class FractalTest(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # create ui
        f = tk.Frame(self, bd=2)

        self.resetButton = tk.Button(f, text='Reset', command=self.on_reset)
        self.resetButton.pack(side='left')

        f.pack(fill='x')

        self.c = tk.Canvas(self, bd=0, highlightthickness=0,
                           width=100, height=100)
        self.c.pack(fill='both', expand=1)
        self.c.bind("<B1-Motion>", self.on_drag)

        # load image
        # im = Image.open('out/fractal.png')
        # im.thumbnail((512, 512))

        im = Image.new("RGB", (W, H), "black")

        self.pic = ImageTk.PhotoImage(im)
        self.canvasItem = self.c.create_image(0, 0, anchor='nw', image=self.pic)
        self.c.config(width=im.size[0], height=im.size[1])

        self.img = im
        self.temp = im.copy()  # 'working' image

        self.pixMap = self.temp.load()
        self.changes = []

    def display_image(self, image):
        self.pic = ImageTk.PhotoImage(image)
        self.c.itemconfigure(self.canvasItem, image=self.pic)

    def on_reset(self):
        self.display_image(self.img)
        self.temp = self.img.copy()
        self.pixMap = self.temp.load()
        self.changes = []

    def on_drag(self, event):
        # print("{}/{}".format(event.x, event.y))
        for (x, y) in self.changes:
            self.draw(x, y, (0, 0, 0))
        self.changes = self.get_pixels(event)
        for (x, y) in self.changes:
            self.draw(x, y, (0, 255, 255))
        self.display_image(self.temp)

    @staticmethod
    def get_pixels(event):
        # return [(event.x - 4 + a, event.y - 4 + b) for a in range(8) for b in range(8)] # square
        l = []
        z, c = 0, translate_c(event.x, event.y)
        for _ in range(MAX_ITERATIONS):
            if abs(z) > 2:
                return l
            z = z ** 2 + c
            l.append(translate_xy(z))
        return l

    def draw(self, x, y, col):
        if 0 <= x < self.img.width and 0 <= y < self.img.height:
            self.pixMap[x, y] = col


FractalTest().mainloop()
