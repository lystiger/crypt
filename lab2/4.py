def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y


def mod_inverse(a, n):
    gcd, x, _ = extended_gcd(a, n)
    if gcd != 1:
        raise ValueError("Inverse does not exist (numbers not coprime)")
    return x % n

a = 65537
N = 35256

print(mod_inverse(a,N))