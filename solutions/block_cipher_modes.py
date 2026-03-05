"""Block cipher modes calculator: ECB, CBC, CTR (AES backend).

Requires: pycryptodome
Install: pip install pycryptodome

Input:
- mode (ecb/cbc/ctr)
- operation (enc/dec)
- key and message in hex
- IV (CBC) or nonce+initial counter (CTR)

Output:
- result bytes in hex
"""

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def ecb_encrypt(key: bytes, plaintext: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(plaintext, AES.block_size))


def ecb_decrypt(key: bytes, ciphertext: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(ciphertext), AES.block_size)


def cbc_encrypt(key: bytes, iv: bytes, plaintext: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(plaintext, AES.block_size))


def cbc_decrypt(key: bytes, iv: bytes, ciphertext: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size)


def ctr_crypt(key: bytes, nonce: bytes, initial_counter: int, data: bytes) -> bytes:
    # CTR encryption and decryption are the same XOR keystream process.
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce, initial_value=initial_counter)
    return cipher.encrypt(data)


def parse_hex(prompt: str) -> bytes:
    return bytes.fromhex(input(prompt).strip())


def parse_key(prompt: str) -> bytes:
    key = parse_hex(prompt)
    if len(key) not in (16, 24, 32):
        raise ValueError("AES key must be 16, 24, or 32 bytes (hex input)")
    return key


if __name__ == "__main__":
    mode = input("Mode (ecb/cbc/ctr): ").strip().lower()
    op = input("Operation (enc/dec): ").strip().lower()

    if mode not in {"ecb", "cbc", "ctr"}:
        raise SystemExit("Mode must be one of: ecb, cbc, ctr")
    if op not in {"enc", "dec"}:
        raise SystemExit("Operation must be one of: enc, dec")

    key = parse_key("Key hex (32/48/64 hex chars): ")

    if mode == "ecb":
        data = parse_hex("Plaintext hex: " if op == "enc" else "Ciphertext hex: ")
        out = ecb_encrypt(key, data) if op == "enc" else ecb_decrypt(key, data)
        print("Output hex:", out.hex())

    elif mode == "cbc":
        iv = parse_hex("IV hex (32 hex chars): ")
        if len(iv) != 16:
            raise SystemExit("IV must be 16 bytes")
        data = parse_hex("Plaintext hex: " if op == "enc" else "Ciphertext hex: ")
        out = cbc_encrypt(key, iv, data) if op == "enc" else cbc_decrypt(key, iv, data)
        print("Output hex:", out.hex())

    else:  # ctr
        nonce = parse_hex("Nonce hex (recommend 8 bytes => 16 hex chars): ")
        counter = int(input("Initial counter (integer): ").strip())
        data = parse_hex("Input hex (plaintext for enc / ciphertext for dec): ")
        out = ctr_crypt(key, nonce, counter, data)
        print("Output hex:", out.hex())
