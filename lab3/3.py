# Encryption 
#C = M^e mod N

# Decryption
# M = C^d mod N

p = 81401
q = 27109
e = 65537
C = 412589464

n = p * q
phi = (p - 1) * (q - 1)

#this is the euclidean algorithm
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x1, y1 = egcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y

#modular inverse
def mod(a,m):
    g,x, _ = egcd(a,m)
    return x % m

d = mod(e, phi)

M = pow(C,d,n)

chars = []
temp = M

while temp > 0:
    chars.append(chr(temp % 256))
    temp //= 256

plaintext = "".join(reversed(chars))

print("Plaintext:", plaintext)