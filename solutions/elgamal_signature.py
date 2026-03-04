"""ElGamal signature: sign and verify.

Input:
- p, alpha, private d
- message x and ephemeral k
Output:
- beta, signature (r,s), verification result
"""

from math import gcd


def egcd(a: int, b: int):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def mod_inverse(a: int, m: int):
    g, x, _ = egcd(a, m)
    if g != 1:
        return None
    return x % m


def sign_elgamal(x: int, p: int, alpha: int, d: int, k: int):
    if gcd(k, p - 1) != 1:
        raise ValueError("k must be coprime with p-1")

    beta = pow(alpha, d, p)
    r = pow(alpha, k, p)
    k_inv = mod_inverse(k, p - 1)
    s = ((x - d * r) * k_inv) % (p - 1)
    return beta, r, s


def verify_elgamal(x: int, r: int, s: int, p: int, alpha: int, beta: int) -> bool:
    if not (1 <= r <= p - 1):
        return False
    left = pow(alpha, x, p)
    right = (pow(beta, r, p) * pow(r, s, p)) % p
    return left == right


if __name__ == "__main__":
    p = int(input("Enter p: ").strip())
    alpha = int(input("Enter alpha: ").strip())
    d = int(input("Enter private key d: ").strip())
    x = int(input("Enter message x: ").strip())
    k = int(input("Enter ephemeral key k: ").strip())

    beta, r, s = sign_elgamal(x, p, alpha, d, k)
    ok = verify_elgamal(x, r, s, p, alpha, beta)

    print("beta =", beta)
    print("signature (r,s) =", (r, s))
    print("valid =", ok)
