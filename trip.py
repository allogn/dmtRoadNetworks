class Trip:
    def __init__(self, src, dst, name=None):
        self.src = src
        self.dst = dst
        self.name = name

    def display(self):
        print("Src: ", self.src, ", Dst: ", self.dst)