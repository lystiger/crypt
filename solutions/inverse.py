"""Extended Euclidean algorithm + modular inverse.

Input:
- a and n
Output:
- gcd(a, n), Bézout coefficients x,y where ax+ny=gcd(a,n)
- modular inverse a^-1 mod n if it exists
"""


def extended_gcd(a: int, b: int):
    if b == 0:
        return abs(a), 1 if a >= 0 else -1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y


def mod_inverse(a: int, n: int):
    g, x, _ = extended_gcd(a, n)
    if g != 1:
        return None
    return x % n


if __name__ == "__main__":
    a = int(input("Enter a: ").strip())
    n = int(input("Enter n: ").strip())

    g, x, y = extended_gcd(a, n)
    print(f"gcd({a}, {n}) = {g}")
    print(f"Bezout: {a}*({x}) + {n}*({y}) = {g}")

    inv = mod_inverse(a, n)
    if inv is None:
        print(f"No modular inverse for {a} mod {n} (not coprime).")
    else:
        print(f"Inverse: {a}^-1 mod {n} = {inv}")
