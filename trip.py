class Trip:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def display(self):
        print("Src: ", self.src, ", Dst: ", self.dst)