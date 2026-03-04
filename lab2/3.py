def square_and_multiply(x, e, n):
    """
    Computes (x^e) mod n using Square-and-Multiply
    """
    result = 1
    x = x % n

    for bit in bin(e)[2:]:   # left-to-right
        result = (result * result) % n  # square
        if bit == '1':
            result = (result * x) % n   # multiply

    return result

x = 856
e = 25
n = 7

print(square_and_multiply(x,e,n))