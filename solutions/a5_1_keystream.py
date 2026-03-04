"""A5/1 keystream generator for exercise-style inputs.

Input:
- Initial X/Y/Z register bitstrings
- Number of output bits
Output:
- Keystream bits and final register states
"""


def majority(a: int, b: int, c: int) -> int:
    return (a & b) | (a & c) | (b & c)


class LFSR:
    def __init__(self, bits: str, taps: list[int], clock_bit: int):
        self.state = [int(ch) for ch in bits]
        self.taps = taps
        self.clock_bit = clock_bit

    def clock(self):
        feedback = 0
        for t in self.taps:
            feedback ^= self.state[t]
        self.state = [feedback] + self.state[:-1]

    def output(self) -> int:
        return self.state[-1]

    def cbit(self) -> int:
        return self.state[self.clock_bit]

    def bits(self) -> str:
        return "".join(map(str, self.state))


def a5_1_generate(x_bits: str, y_bits: str, z_bits: str, n_bits: int):
    x = LFSR(x_bits, [13, 16, 17, 18], 8)
    y = LFSR(y_bits, [20, 21], 10)
    z = LFSR(z_bits, [7, 20, 21, 22], 10)

    out = []
    for _ in range(n_bits):
        # Output bit is from current states (as many exam questions require).
        out.append(x.output() ^ y.output() ^ z.output())

        m = majority(x.cbit(), y.cbit(), z.cbit())
        if x.cbit() == m:
            x.clock()
        if y.cbit() == m:
            y.clock()
        if z.cbit() == m:
            z.clock()

    return out, x.bits(), y.bits(), z.bits()


if __name__ == "__main__":
    x_bits = input("Enter X (19 bits): ").strip()
    y_bits = input("Enter Y (22 bits): ").strip()
    z_bits = input("Enter Z (23 bits): ").strip()
    n = int(input("How many keystream bits? ").strip())

    ks, x_end, y_end, z_end = a5_1_generate(x_bits, y_bits, z_bits, n)
    print("Keystream:", "".join(map(str, ks)))
    print("X after generation:", x_end)
    print("Y after generation:", y_end)
    print("Z after generation:", z_end)
