"""SHA-1 block structure generator from input message.

What it does:
- Reads a message (UTF-8 text)
- Applies SHA-1 padding (1 bit, zeros, 64-bit length)
- Splits padded message into 512-bit blocks
- Prints per-block structure and hex view
- Prints final SHA-1 digest for reference
"""

import hashlib


def bytes_to_bitstring(data: bytes) -> str:
    return "".join(f"{b:08b}" for b in data)


def sha1_pad(message: bytes) -> bytes:
    bit_len = len(message) * 8

    # Append '1' bit => byte 0x80
    padded = message + b"\x80"

    # Add zero bytes until length is 56 mod 64 bytes (448 mod 512 bits).
    while len(padded) % 64 != 56:
        padded += b"\x00"

    # Append original length as 64-bit big-endian integer.
    padded += bit_len.to_bytes(8, "big")
    return padded


def split_blocks(data: bytes, block_size: int = 64) -> list[bytes]:
    return [data[i:i + block_size] for i in range(0, len(data), block_size)]


def print_block_info(block: bytes, index: int):
    words = [int.from_bytes(block[i:i + 4], "big") for i in range(0, 64, 4)]

    print(f"Block {index} (512 bits / 64 bytes)")
    print("Hex:", block.hex())
    print("Words W0..W15 (32-bit, hex):")
    print(" ".join(f"{w:08x}" for w in words))


def explain_structure(message: bytes):
    original_bits = len(message) * 8
    padded = sha1_pad(message)
    padded_bits = len(padded) * 8
    blocks = split_blocks(padded)

    # k is the number of zero bits between the appended 1-bit and 64-bit length field.
    # Since we build with bytes, this still corresponds to SHA-1 definition.
    k = (448 - (original_bits + 1) % 512) % 512

    print("SHA-1 preprocessing")
    print(f"Original length L: {original_bits} bits")
    print("Format: M || 1 || 0^k || [L]_64")
    print(f"k = {k} zero bits")
    print(f"Padded length: {padded_bits} bits")
    print(f"Number of 512-bit blocks: {len(blocks)}")
    print()

    for i, block in enumerate(blocks):
        print_block_info(block, i)
        print()

    digest = hashlib.sha1(message).hexdigest()
    print("SHA-1 digest:", digest)


if __name__ == "__main__":
    msg = input("Enter message text: ").encode("utf-8")
    explain_structure(msg)
