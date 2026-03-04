"""Explain SHA-1 preprocessing (padding) for a message length in bits.

Input:
- Original message length L (in bits)
Output:
- Number of zero bits added
- Total padded length
- Number of 512-bit blocks
- Format: M || 1 || 0...0 || [L]_64
"""


def sha1_padding_info(message_bits: int):
    if message_bits < 0:
        raise ValueError("Message length must be non-negative")

    # After appending one '1' bit, add k zero bits so total is 448 mod 512.
    k = (448 - (message_bits + 1) % 512) % 512
    total_length = message_bits + 1 + k + 64
    blocks = total_length // 512

    return {
        "L": message_bits,
        "one_bit": 1,
        "zero_bits": k,
        "length_field_bits": 64,
        "total_bits": total_length,
        "blocks": blocks,
        "format": "M || 1 || 0^k || [L]_64",
    }


if __name__ == "__main__":
    L = int(input("Enter message length L (bits): ").strip())
    info = sha1_padding_info(L)

    print("SHA-1 padding result")
    print("L =", info["L"], "bits")
    print("Append 1 bit =", info["one_bit"])
    print("Append 0 bits =", info["zero_bits"])
    print("Append length field =", info["length_field_bits"], "bits")
    print("Total padded length =", info["total_bits"], "bits")
    print("Number of 512-bit blocks =", info["blocks"])
    print("Padded message format:", info["format"])
