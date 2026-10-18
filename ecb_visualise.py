"""
Challenge Lab 6 - AES-ECB Encrypted Bitmap
Zihan Izhar Bin Azahir (A00083538) & Ian Njagi (A00083580)

1. Writes a valid 640x480 24-bit BMP header over the encrypted one (fixed.bmp).
2. Builds a high-contrast image: the most common 16-byte ciphertext block
   (the encrypted background) becomes white, every other block black (clean.bmp).

Usage: python3 ecb_visualise.py [aes.bmp.enc]
"""
import collections
import struct
import sys

SRC = sys.argv[1] if len(sys.argv) > 1 else "aes.bmp.enc"
WIDTH, HEIGHT, BPP = 640, 480, 24
HEADER_LEN = 54
BLOCK = 16


def bmp_header(w, h, bpp=24):
    row = ((w * bpp // 8) + 3) & ~3
    size = row * h
    return (b"BM" + struct.pack("<IHHI", HEADER_LEN + size, 0, 0, HEADER_LEN) +
            struct.pack("<IiiHHIIiiII", 40, w, h, 1, bpp, 0, size, 2835, 2835, 0, 0))


data = open(SRC, "rb").read()
body = data[HEADER_LEN:]
assert len(body) == WIDTH * HEIGHT * 3, "unexpected file size"

# 1) Raw view: valid header + untouched encrypted pixels
with open("fixed.bmp", "wb") as f:
    f.write(bmp_header(WIDTH, HEIGHT) + body)

# 2) High-contrast view
blocks = [body[i:i + BLOCK] for i in range(0, len(body) - len(body) % BLOCK, BLOCK)]
counts = collections.Counter(blocks)
background = counts.most_common(1)[0][0]
mapped = b"".join(b"\xff" * BLOCK if b == background else b"\x00" * BLOCK for b in blocks)
mapped += b"\x00" * (len(body) - len(mapped))
with open("clean.bmp", "wb") as f:
    f.write(bmp_header(WIDTH, HEIGHT) + mapped)

print(f"Unique blocks: {len(counts)} of {len(blocks)}")
print(f"Background block: {background.hex()}")
print("Wrote fixed.bmp and clean.bmp")
