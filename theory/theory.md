# Introduction to Cryptography - Past Test Theory Notes

This document consolidates recurring theory and solving patterns from the past tests in `pics/`.

## 1. Euclidean Algorithms and Modular Inverse

### GCD (Euclidean algorithm)
- Core recurrence: `gcd(a, b) = gcd(b, a mod b)`.
- Stop when remainder is `0`.
- Last non-zero remainder is the gcd.

### Extended Euclidean algorithm
- Finds integers `x, y` such that:
  `ax + by = gcd(a, b)`.
- For modular inverse in `mod n`:
  `a^-1 mod n` exists iff `gcd(a, n) = 1`.
- Then `a^-1 ≡ x (mod n)` where `ax + ny = 1`.

## 2. Fast Modular Exponentiation (Repeated Squaring / Square-and-Multiply)

Goal: compute `x^e mod n` efficiently.

- Write `e` in binary.
- Repeatedly square current result.
- Multiply by `x` when current exponent bit is `1`.

Negative exponent case:
- `x^-1 mod n` must exist (`gcd(x, n)=1`).
- `x^(-k) mod n = (x^-1)^k mod n`.

## 3. RSA Cryptosystem

### Key generation
1. Choose primes `p, q`.
2. Compute `N = p*q`.
3. Compute `phi(N) = (p-1)(q-1)`.
4. Choose public exponent `e` such that:
   - `1 < e < phi(N)`
   - `gcd(e, phi(N)) = 1`
5. Compute private exponent `d = e^-1 mod phi(N)`.
6. Public key: `(N, e)`, private key: `(N, d)`.

### Encryption and decryption
- Encrypt: `C = M^e mod N`
- Decrypt: `M = C^d mod N`

### Typical exam checks
- Given two `e` candidates, pick the valid one using gcd test.
- Compute `d` via modular inverse.
- Verify encrypt/decrypt round-trip.

## 4. ElGamal Signature

Parameters: prime `p`, generator `alpha`, private key `d`.
Public key: `beta = alpha^d mod p`.

### Signature generation for message `x`
1. Pick ephemeral `k_E` with `gcd(k_E, p-1) = 1`.
2. Compute `r = alpha^k_E mod p`.
3. Compute `s = k_E^-1 * (x - d*r) mod (p-1)`.
4. Signature is `(r, s)`.

### Signature verification
Check:
`alpha^x mod p == (beta^r * r^s) mod p`.

### Reused exam patterns
- Compute `(r,s)` for given `x, k_E`.
- Verify whether provided signed tuples originate from Bob.
- CA certificate tasks based on ElGamal signatures.

## 5. Certificate Pattern in Tests (CA + ElGamal)

Common pattern in papers:
- Given IDs: `ID(A), ID(B)`.
- Given user values (often DH-related): `k_A, k_B` or `b_A, b_B`.
- CA computes certificate message:
  `x_i = c * value_i + ID(i)` where `c` is provided (e.g., 4 or 5).
- CA signs `x_i` using ElGamal with separate ephemeral keys for A and B.
- Verify each certificate using ElGamal verification equation.

## 6. Diffie-Hellman Key Exchange (DHKE)

Given prime `p`, generator `g`, private exponents `a, b`.

1. Alice public: `K_A = g^a mod p`
2. Bob public: `K_B = g^b mod p`
3. Alice shared: `K_AB(left) = K_B^a mod p`
4. Bob shared: `K_AB(right) = K_A^b mod p`

Validity conclusion:
- Protocol result is valid if `K_AB(left) == K_AB(right)`.

## 7. A5/1 Stream Cipher (Exam-Oriented)

Three LFSRs with irregular clocking and majority vote.

- Compute majority of the three clocking bits.
- Clock each register whose clocking bit equals majority.
- Keystream bit is XOR of selected output bits from three registers.

Typical question:
- Given initial `X, Y, Z` register contents.
- Output first few keystream bits.
- Give new register states after those bits.

## 8. SHA-1 Preprocessing / Padding

For original message length `L` bits:
- Append `1` bit.
- Append `k` zero bits so that `L + 1 + k ≡ 448 (mod 512)`.
- Append 64-bit big-endian length field `[L]_64`.

Final form:
`M || 1 || 0^k || [L]_64`

Block structure:
- Total padded length is multiple of 512 bits.
- Split into 512-bit blocks.
- Each block has 16 words (`W0..W15`) of 32 bits.

## 9. Hash from Block Cipher (Construction Question)

Frequently appears as formula-only and diagram question, e.g.:
- `H_i = e(x_i XOR H_{i-1}, x_i) XOR H_{i-1}`
- or `H_i = e(x_i XOR H_{i-1}, x_i) XOR x_i`

What to know:
- Inputs to block cipher `e()` are clearly identified by formula.
- XOR feedback determines how chaining state updates.
- Draw dataflow with `x_i`, `H_{i-1}`, cipher block, and output XOR node.

## 10. DES (High-Level Features)

When DES theory is asked:
- Block size: 64 bits
- Key length: 64 bits total
- Effective key length: 56 bits (8 parity bits)
- Rounds: 16 Feistel rounds
- Round subkey length: 48 bits

## 11. Common Exam Workflow Strategy

1. Identify the primitive (RSA / ElGamal / DHKE / hash / A5/1).
2. Write formulas first.
3. Check validity conditions early:
   - Coprime checks for inverses and exponents.
   - Range checks for signature values.
4. Compute with modular arithmetic carefully.
5. For verification tasks, compare both sides explicitly.
6. State final validity conclusion clearly (`valid / invalid`).

## 12. Quick Formula Sheet

- `gcd(a,b)` via Euclidean recursion.
- `a^-1 mod n` exists iff `gcd(a,n)=1`.
- RSA: `N=pq`, `phi=(p-1)(q-1)`, `d=e^-1 mod phi`.
- RSA encrypt/decrypt: `C=M^e mod N`, `M=C^d mod N`.
- ElGamal: `beta=alpha^d mod p`, `r=alpha^k mod p`,
  `s=k^-1(x-dr) mod (p-1)`.
- ElGamal verify: `alpha^x ≡ beta^r * r^s (mod p)`.
- DHKE shared key: `(g^b)^a mod p = (g^a)^b mod p`.
- SHA-1 padding: `M || 1 || 0^k || [L]_64` with
  `L+1+k ≡ 448 (mod 512)`.
