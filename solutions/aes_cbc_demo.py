"""AES-CBC encryption/decryption demo.

Requires: pycryptodome (pip install pycryptodome)
Input:
- key (16/24/32 bytes as text), IV (16 bytes as text), plaintext
Output:
- ciphertext (hex) and recovered plaintext
"""

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
except ImportError as exc:
    raise SystemExit(
        "This script needs pycryptodome. Install with: pip install pycryptodome"
    ) from exc


def aes_cbc_encrypt(key: bytes, iv: bytes, plaintext: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(plaintext, AES.block_size))


def aes_cbc_decrypt(key: bytes, iv: bytes, ciphertext: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size)


if __name__ == "__main__":
    key = input("Key (16/24/32 chars): ").encode("utf-8")
    iv = input("IV (16 chars): ").encode("utf-8")
    message = input("Plaintext: ").encode("utf-8")

    if len(key) not in (16, 24, 32):
        raise SystemExit("Key must be 16, 24, or 32 bytes")
    if len(iv) != 16:
        raise SystemExit("IV must be exactly 16 bytes")

    ct = aes_cbc_encrypt(key, iv, message)
    pt = aes_cbc_decrypt(key, iv, ct)

    print("Ciphertext (hex):", ct.hex())
    print("Recovered plaintext:", pt.decode("utf-8", errors="replace"))
