"""HKDF-SHA256 (RFC 5869 style) using only Python standard library.

Input:
- input keying material (ikm), salt, info, output length
Output:
- derived key (hex)
"""

import hashlib
import hmac


def hkdf_extract(salt: bytes, ikm: bytes) -> bytes:
    # PRK = HMAC(salt, IKM)
    return hmac.new(salt, ikm, hashlib.sha256).digest()


def hkdf_expand(prk: bytes, info: bytes, length: int) -> bytes:
    hash_len = hashlib.sha256().digest_size
    if length > 255 * hash_len:
        raise ValueError("Requested length too large")

    t = b""
    okm = b""
    counter = 1

    while len(okm) < length:
        t = hmac.new(prk, t + info + bytes([counter]), hashlib.sha256).digest()
        okm += t
        counter += 1

    return okm[:length]


def hkdf(ikm: bytes, salt: bytes, info: bytes, length: int) -> bytes:
    prk = hkdf_extract(salt, ikm)
    return hkdf_expand(prk, info, length)


if __name__ == "__main__":
    ikm = input("IKM (utf-8 text): ").encode("utf-8")
    salt = input("Salt (utf-8 text): ").encode("utf-8")
    info = input("Info (utf-8 text): ").encode("utf-8")
    length = int(input("Output length in bytes: ").strip())

    out = hkdf(ikm, salt, info, length)
    print("Derived key (hex):", out.hex())
