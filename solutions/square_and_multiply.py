"""Fast modular exponentiation using square-and-multiply.

Input:
- base x, exponent e, modulus n
Output:
- x^e mod n
"""


def square_and_multiply(x: int, e: int, n: int) -> int:
    if n <= 0:
        raise ValueError("Modulus n must be positive")

    # For negative exponents, use modular inverse:
    # x^(-e) mod n = (x^-1)^e mod n, if inverse exists.
    if e < 0:
        x = pow(x, -1, n)  # Raises ValueError when inverse does not exist.
        e = -e

    result = 1
    x %= n

    # Left-to-right binary exponentiation.
    for bit in bin(e)[2:]:
        result = (result * result) % n
        if bit == "1":
            result = (result * x) % n
    return result


if __name__ == "__main__":
    x = int(input("Enter x: ").strip())
    e = int(input("Enter e: ").strip())
    n = int(input("Enter n: ").strip())
    print(f"{x}^{e} mod {n} = {square_and_multiply(x, e, n)}")
