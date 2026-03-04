"""Generate and verify simple CA certificates using ElGamal signatures.

This follows the exam pattern:
- user chooses b_i for DH public value y_i = alpha^b_i mod p
- CA computes x_i = factor * b_i + ID(i)
- CA signs x_i with ElGamal
"""

from elgamal_signature import sign_elgamal, verify_elgamal


def make_certificate(name: str, user_id: int, b: int, factor: int, ca_p: int, ca_alpha: int, ca_d: int, ca_k: int):
    x = factor * b + user_id
    beta_ca, r, s = sign_elgamal(x, ca_p, ca_alpha, ca_d, ca_k)
    return {
        "name": name,
        "id": user_id,
        "b": b,
        "x": x,
        "ca_pub": (ca_p, ca_alpha, beta_ca),
        "signature": (r, s),
    }


def verify_certificate(cert: dict) -> bool:
    p, alpha, beta = cert["ca_pub"]
    r, s = cert["signature"]
    return verify_elgamal(cert["x"], r, s, p, alpha, beta)


if __name__ == "__main__":
    # Example values from exam-style settings.
    ca_p = int(input("Enter CA prime p: ").strip())
    ca_alpha = int(input("Enter CA alpha: ").strip())
    ca_d = int(input("Enter CA private d: ").strip())
    factor = int(input("Enter x_i factor (e.g. 4 or 5): ").strip())

    id_a = int(input("Enter ID(A): ").strip())
    b_a = int(input("Enter bA: ").strip())
    k_a = int(input("Enter CA ephemeral k for A: ").strip())

    id_b = int(input("Enter ID(B): ").strip())
    b_b = int(input("Enter bB: ").strip())
    k_b = int(input("Enter CA ephemeral k for B: ").strip())

    cert_a = make_certificate("Alice", id_a, b_a, factor, ca_p, ca_alpha, ca_d, k_a)
    cert_b = make_certificate("Bob", id_b, b_b, factor, ca_p, ca_alpha, ca_d, k_b)

    print("CertA:", cert_a)
    print("CertA valid:", verify_certificate(cert_a))
    print("CertB:", cert_b)
    print("CertB valid:", verify_certificate(cert_b))
