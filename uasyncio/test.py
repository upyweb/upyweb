import uheapq as heapq

N = 256

class Mod:

    def __init__(self, n):
        self.n = n

    def __str__(self):
        return "Mod(%d)" % self.n

    def __lt__(self, other):
        print("%s < %s" % (self, other))
        v = other.n - self.n
        if v < 0:
            v += N
        print("%d < %d" % (v, N / 2))
        return v < N / 2


print(Mod(255) < Mod(0))
