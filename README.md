# Challenge Lab 6 – AES-ECB Encrypted Bitmap

**Module:** Secure Communication and Cryptography (MACS H6014)
**Students:** Zihan Izhar Bin Azahir (A00083538) & Ian Njagi (A00083580)

The bitmap `aes.bmp.enc` was encrypted with AES in ECB mode. Because ECB encrypts
identical 16-byte blocks to identical ciphertext, the image outline survives.
Replacing the encrypted 54-byte BMP header with a valid one reveals the flag.

**Flag:** `flag{Tro11d}`

## Files
| File | Purpose |
|------|---------|
| `fix_header.sh` | Kali Linux method (`file`, `xxd`, `printf`, `dd`) – writes `fixed.bmp` |
| `ecb_visualise.py` | Python method – writes `fixed.bmp` and high-contrast `clean.bmp` |

## Reproduce
```bash
chmod +x fix_header.sh
./fix_header.sh aes.bmp.enc fixed.bmp
# or
python3 ecb_visualise.py aes.bmp.enc
```
