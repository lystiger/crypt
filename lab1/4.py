def majority(a,b,c):
    return (a & b) | ( a&c) | (b & c)

class LFSR:
    def __init__(self, value, size, taps, clock_bit):
        self.size = size
        self.taps = taps
        self.clock_bit = clock_bit
        self.state = [(value >> i) & 1 for i in range(size)]

    def clock(self):
        feedback = 0
        for t in self.taps:
            feedback ^= self.state[t]
        self.state = [feedback] + self.state[:-1]

    def output(self):
        return self.state[-1]

    def clocking_bit(self):
        return self.state[self.clock_bit]

def a5_1_keystream(X0, Y0, Z0, n):
    X = LFSR(X0, 19, [13, 16, 17, 18], 8)
    Y = LFSR(Y0, 22, [20, 21], 10)
    Z = LFSR(Z0, 23, [7, 20, 21, 22], 10)

    keystream = []

    for _ in range(n):
        m = majority(X.clocking_bit(), Y.clocking_bit(), Z.clocking_bit())

        if X.clocking_bit() == m:
            X.clock()
        if Y.clocking_bit() == m:
            Y.clock()
        if Z.clocking_bit() == m:
            Z.clock()

        bit = X.output() ^ Y.output() ^ Z.output()
        keystream.append(bit)

    return keystream


X0 = 513365
Y0 = 3355443
Z0 = 7401712
n = 10

ks = a5_1_keystream(X0, Y0, Z0, n)
print("Keystream:", ks)

