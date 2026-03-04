"""Compute iterative hash built from a block cipher-like function.

Exam formulas seen in your pictures include:
- H_i = e(x_i XOR H_{i-1}, x_i) XOR H_{i-1}
- H_i = e(x_i XOR H_{i-1}, x_i) XOR x_i

This script supports both variants for numerical toy exercises.
"""


def toy_block_cipher(m: int, k: int, mod: int) -> int:
    # Toy stand-in for e(m,k): deterministic and reversible-looking math.
    # Real exercises usually ask for block diagram, not concrete numeric output.
    return ((m ^ k) + (3 * k + 7)) % mod


def compute_hash(blocks: list[int], h0: int, mod: int, xor_with: str):
    if xor_with not in {"h_prev", "x_i"}:
        raise ValueError("xor_with must be 'h_prev' or 'x_i'")

    h = h0
    trace = []

    for i, x_i in enumerate(blocks, start=1):
        c_in = x_i ^ h
        e_out = toy_block_cipher(c_in, x_i, mod)
        if xor_with == "h_prev":
            h_new = e_out ^ h
            formula = "H_i = e(x_i XOR H_{i-1}, x_i) XOR H_{i-1}"
        else:
            h_new = e_out ^ x_i
            formula = "H_i = e(x_i XOR H_{i-1}, x_i) XOR x_i"

        trace.append((i, x_i, h, c_in, e_out, h_new))
        h = h_new

    return h, formula, trace


if __name__ == "__main__":
    mod = int(input("Bit-width modulus (e.g. 256 for 8-bit toy): ").strip())
    h0 = int(input("Initial value H0: ").strip())
    blocks = list(map(int, input("Message blocks x_i (space-separated integers): ").split()))
    xor_with = input("Variant ('h_prev' or 'x_i'): ").strip()

    h_final, formula, trace = compute_hash(blocks, h0, mod, xor_with)

    print("Using:", formula)
    print("Trace columns: i, x_i, H_{i-1}, (x_i XOR H_{i-1}), e_out, H_i")
    for row in trace:
        print(row)
    print("Final hash H_n =", h_final)
