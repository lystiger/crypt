"""Diffie-Hellman key exchange demo.

Input:
- prime p, generator g
- private exponents a and b
Output:
- public values A, B and shared secret from both sides
"""


def dhke(p: int, g: int, a: int, b: int):
    a_pub = pow(g, a, p)
    b_pub = pow(g, b, p)

    secret_alice = pow(b_pub, a, p)
    secret_bob = pow(a_pub, b, p)

    return a_pub, b_pub, secret_alice, secret_bob


if __name__ == "__main__":
    p = int(input("Enter prime p: ").strip())
    g = int(input("Enter generator g: ").strip())
    a = int(input("Enter Alice private a: ").strip())
    b = int(input("Enter Bob private b: ").strip())

    A, B, s1, s2 = dhke(p, g, a, b)
    print("Alice public A =", A)
    print("Bob public B =", B)
    print("Alice shared secret =", s1)
    print("Bob shared secret =", s2)
    print("Match:", s1 == s2)
