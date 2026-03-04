import math
A = [290345, 218585, 143231, 164172, 155768, 423151, 239707, 153544, 287390, 480837]

pairs = []

for i in range(len (A)):
    for j in range (i + 1, len(A)):
        if math.gcd(A[i], A[j]) == 1:
            pairs.append((A[i], A[j]))

print("All pairs of prime number are:", pairs)

