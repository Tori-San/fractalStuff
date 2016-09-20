class Bar:

    def __init__(self, left="[", right="]", full="#", empty=" ", length=40):
        self.left = left
        self.right = right
        self.full = full
        self.empty = empty
        self.length = length
        self.progress = 0
    
    def start(self):
        print(self.left + self.length * self.empty + self.right, end="")

    def update(self, x):
        progress = int(self.length * x + 0.5)
        if progress > self.progress:
            self.progress = progress
            print("\r", end="")
            print(self.left +
                  self.progress * self.full +
                  (self.length - self.progress) * self.empty +
                  self.right +
                  " {:.2f}%".format(100*x).rjust(6), end="")

    def end(self):
        print("\r", end="")
        print(self.left + self.length * self.full + self.right + 7*" ")
