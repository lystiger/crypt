"""Compute GCD with the Euclidean algorithm.

Input:
- Two integers a and b.
Output:
- gcd(a, b)
"""


def euclidean_gcd(a: int, b: int) -> int:
    # Repeatedly replace (a, b) by (b, a mod b) until b becomes 0.
    while b != 0:
        a, b = b, a % b
    return abs(a)


if __name__ == "__main__":
    a = int(input("Enter a: ").strip())
    b = int(input("Enter b: ").strip())
    print(f"gcd({a}, {b}) = {euclidean_gcd(a, b)}")
