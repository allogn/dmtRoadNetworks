from path import distance

class Client:
    def __init__(self, src, dst, name=None):
        self.src = src
        self.dst = dst
        self.dist = distance(src,dst)
        self.name = name

    def display(self):
        print('Name: ', self.name, "Src: ", self.src, ", Dst: ", self.dst)