"""RSA helper for exam exercises.

Features:
- Validate candidate exponents e by gcd(e, phi)=1
- Compute d = e^-1 mod phi
- Encrypt and decrypt one plaintext M
"""

from math import gcd


def extended_gcd(a: int, b: int):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def mod_inverse(a: int, n: int):
    g, x, _ = extended_gcd(a, n)
    if g != 1:
        return None
    return x % n


def rsa_solve(p: int, q: int, e_candidates: list[int], m: int):
    n = p * q
    phi = (p - 1) * (q - 1)

    valid = [e for e in e_candidates if 1 < e < phi and gcd(e, phi) == 1]
    if not valid:
        raise ValueError("No valid exponent found")

    e = valid[0]
    d = mod_inverse(e, phi)
    c = pow(m, e, n)
    m_dec = pow(c, d, n)

    return {
        "n": n,
        "phi": phi,
        "valid_exponents": valid,
        "chosen_e": e,
        "d": d,
        "ciphertext": c,
        "decrypted": m_dec,
    }


if __name__ == "__main__":
    p = int(input("Enter p: ").strip())
    q = int(input("Enter q: ").strip())
    e_candidates = list(map(int, input("Enter e candidates (space-separated): ").split()))
    m = int(input("Enter plaintext M: ").strip())

    data = rsa_solve(p, q, e_candidates, m)
    print("N =", data["n"])
    print("phi(N) =", data["phi"])
    print("Valid e values =", data["valid_exponents"])
    print("Chosen e =", data["chosen_e"])
    print("d =", data["d"])
    print("Ciphertext C =", data["ciphertext"])
    print("Decrypted M =", data["decrypted"])
