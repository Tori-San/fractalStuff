class Bar:

    def __init__(self, left="[", right="]", full="#", empty=" ", length=40):
        self.left = left
        self.right = right
        self.full = full
        self.empty = empty
        self.length = length
        self.totalLength = len(left) + length + len(right)
        self.progress = 0

    def update(self, x):
        progress = int(self.length * x + 0.5)
        if progress > self.progress:
            self.progress = progress
            print("\r" * self.totalLength, end="")
            print(self.left + self.progress * self.full + (self.length - self.progress) * self.empty + self.right, end="")

    def end(self):
        print("\r" * self.totalLength, end="")
        print(self.left + self.length * self.full + self.right)
