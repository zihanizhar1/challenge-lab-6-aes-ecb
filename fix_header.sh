#!/usr/bin/env bash
# Challenge Lab 6 - AES-ECB Encrypted Bitmap
# Zihan Izhar Bin Azahir (A00083538) & Ian Njagi (A00083580)
#
# Replaces the encrypted 54-byte BMP header of aes.bmp.enc with a valid
# 640x480 24-bit header so the ECB-encrypted pixel data can be viewed.
#
# Usage: ./fix_header.sh [input] [output]
set -euo pipefail

IN="${1:-aes.bmp.enc}"
OUT="${2:-fixed.bmp}"

# 1. Identify the file and look for repeating 16-byte ECB blocks
file "$IN"
xxd "$IN" | head -20

# 2. Confirm the image size: file size - 54-byte header = 640 * 480 * 3
SIZE=$(stat -c %s "$IN")
echo "File size: $SIZE  | pixel bytes: $(( SIZE - 54 ))  | 640*480*3 = $(( 640 * 480 * 3 ))"

# 3. Work on a copy
cp "$IN" "$OUT"

# 4. Write a valid BITMAPFILEHEADER + BITMAPINFOHEADER (54 bytes) over the old one
printf '\x42\x4d\x36\x10\x0e\x00\x00\x00\x00\x00\x36\x00\x00\x00\x28\x00\x00\x00\x80\x02\x00\x00\xe0\x01\x00\x00\x01\x00\x18\x00\x00\x00\x00\x00\x00\x10\x0e\x00\x13\x0b\x00\x00\x13\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
  | dd of="$OUT" bs=1 seek=0 conv=notrunc

# 5. Verify and open
file "$OUT"
xdg-open "$OUT" >/dev/null 2>&1 || echo "Open $OUT in any image viewer."
