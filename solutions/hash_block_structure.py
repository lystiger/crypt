"""SHA-1 block structure generator from input message.

What it does:
- Reads a message (UTF-8 text)
- Applies SHA-1 padding (1 bit, zeros, 64-bit length)
- Splits padded message into 512-bit blocks
- Prints per-block structure and hex view
- Draws the block structure with matplotlib and saves a PNG
- Prints final SHA-1 digest for reference
"""

import hashlib
from textwrap import wrap


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


def split_words(block: bytes, word_bits: int) -> list[int]:
    if word_bits % 8 != 0:
        raise ValueError("word_bits must be a multiple of 8")
    word_bytes = word_bits // 8
    if len(block) % word_bytes != 0:
        raise ValueError("Block size must be divisible by word size")
    return [
        int.from_bytes(block[i:i + word_bytes], "big")
        for i in range(0, len(block), word_bytes)
    ]


def print_block_info(block: bytes, index: int, word_bits: int):
    words = split_words(block, word_bits)
    word_hex_len = word_bits // 4

    print(f"Block {index} ({len(block) * 8} bits / {len(block)} bytes)")
    print("Hex:", block.hex())
    print(f"Words W0..W{len(words)-1} ({word_bits}-bit, hex):")
    print(" ".join(f"{w:0{word_hex_len}x}" for w in words))


def visualize_blocks(blocks: list[bytes], output_path: str, word_bits: int):
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise SystemExit(
            "matplotlib is required for visualization. Install with: pip install matplotlib"
        ) from exc

    rows = len(blocks)
    fig, axes = plt.subplots(rows, 1, figsize=(14, 4 * rows))
    if rows == 1:
        axes = [axes]

    for i, block in enumerate(blocks):
        ax = axes[i]
        words = split_words(block, word_bits)
        word_hex_len = word_bits // 4
        cols = min(4, len(words))
        rows_grid = (len(words) + cols - 1) // cols
        cell_text = []
        idx = 0
        for _ in range(rows_grid):
            row = []
            for _ in range(cols):
                if idx < len(words):
                    row.append(f"W{idx}\n{words[idx]:0{word_hex_len}x}")
                else:
                    row.append("")
                idx += 1
            cell_text.append(row)

        ax.axis("off")
        ax.set_title(f"Block {i} ({len(block) * 8} bits, {word_bits}-bit words)", fontsize=12, pad=12)

        table = ax.table(cellText=cell_text, loc="center", cellLoc="center")
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.1, 2.2)

        # Show full block hex in wrapped lines below each table.
        wrapped_hex = "\n".join(wrap(block.hex(), 64))
        ax.text(
            0.5,
            -0.24,
            f"Block {i} hex:\n{wrapped_hex}",
            transform=ax.transAxes,
            ha="center",
            va="top",
            fontsize=9,
            family="monospace",
        )

    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def explain_structure(message: bytes, image_path: str, block_bits: int, word_bits: int):
    original_bits = len(message) * 8
    padded = sha1_pad(message)
    padded_bits = len(padded) * 8
    if block_bits % 8 != 0:
        raise ValueError("block_bits must be a multiple of 8")
    if word_bits % 8 != 0:
        raise ValueError("word_bits must be a multiple of 8")
    if block_bits % word_bits != 0:
        raise ValueError("block_bits must be divisible by word_bits")
    blocks = split_blocks(padded, block_bits // 8)

    # k is the number of zero bits between the appended 1-bit and 64-bit length field.
    # Since we build with bytes, this still corresponds to SHA-1 definition.
    k = (448 - (original_bits + 1) % 512) % 512

    print("SHA-1 preprocessing")
    print(f"Original length L: {original_bits} bits")
    print("Format: M || 1 || 0^k || [L]_64")
    print(f"k = {k} zero bits")
    print(f"Padded length: {padded_bits} bits")
    print(f"Number of {block_bits}-bit blocks: {len(blocks)}")
    print()

    for i, block in enumerate(blocks):
        print_block_info(block, i, word_bits)
        print()

    digest = hashlib.sha1(message).hexdigest()
    print("SHA-1 digest:", digest)
    visualize_blocks(blocks, image_path, word_bits)
    print(f"Saved block structure image: {image_path}")


def explain_length_only(original_bits: int, block_bits: int, length_field_bits: int = 64):
    if original_bits < 0:
        raise ValueError("original_bits must be non-negative")
    if block_bits <= 0:
        raise ValueError("block_bits must be positive")
    if length_field_bits <= 0:
        raise ValueError("length_field_bits must be positive")

    # SHA-style padding math using explicit bit length L.
    target = block_bits - length_field_bits
    k = (target - (original_bits + 1) % block_bits) % block_bits
    total_bits = original_bits + 1 + k + length_field_bits
    blocks = total_bits // block_bits

    print("Padding (length-only mode)")
    print(f"Original length L: {original_bits} bits")
    print(f"Format: M || 1 || 0^k || [L]_{length_field_bits}")
    print(f"k = {k} zero bits")
    print(f"Total padded length = {total_bits} bits")
    print(f"Number of {block_bits}-bit blocks = {blocks}")


if __name__ == "__main__":
    mode = input("Mode ('message' or 'length') [message]: ").strip().lower() or "message"
    block_bits_raw = input("Block size in bits [512]: ").strip()
    word_bits_raw = input("Word size in bits [32] (use 64 if needed): ").strip()
    block_bits = int(block_bits_raw) if block_bits_raw else 512
    word_bits = int(word_bits_raw) if word_bits_raw else 32
    if mode == "length":
        l_bits = int(input("Original message length L (bits): ").strip())
        length_field_raw = input("Length-field size in bits [64]: ").strip()
        length_field_bits = int(length_field_raw) if length_field_raw else 64
        explain_length_only(l_bits, block_bits, length_field_bits)
    else:
        msg = input("Enter message text: ").encode("utf-8")
        output = input("Output image path [hash_blocks.png]: ").strip() or "hash_blocks.png"
        explain_structure(msg, output, block_bits, word_bits)
