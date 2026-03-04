"""List all coprime pairs in a list of integers.

Input:
- Space-separated integers
Output:
- All pairs (ai, aj) where gcd(ai, aj) = 1
"""

from math import gcd


def find_coprime_pairs(values):
    pairs = []
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            if gcd(values[i], values[j]) == 1:
                pairs.append((values[i], values[j]))
    return pairs


if __name__ == "__main__":
    values = list(map(int, input("Enter integers (space-separated): ").split()))
    pairs = find_coprime_pairs(values)
    print("Coprime pairs:")
    for p in pairs:
        print(p)
