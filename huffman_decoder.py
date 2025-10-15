# ==============================================================
# Program   : Huffman Decoder 
# Author    : Rahmatul Zikri
# Deskripsi :
#   - Membaca hasil encoding dari encoded.txt dan codes.txt
#   - Mengembalikan teks asli (decode)
# ==============================================================

import os
import json

# ======== Tentukan lokasi folder yang sama ========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
encoded_path = os.path.join(BASE_DIR, "encoded.txt")
codes_path   = os.path.join(BASE_DIR, "codes.txt")
decoded_path = os.path.join(BASE_DIR, "decoded.txt")

# ========  Fungsi untuk decoding Huffman ========
def huffman_decode(encoded_text, codes):
    # Buat peta kebalikan: biner → karakter
    reverse_code = {v: k for k, v in codes.items()}
    decoded = ""
    temp = ""
    for bit in encoded_text:
        if bit not in ("0", "1"):
            # abaikan karakter newline atau spasi dari encoded.txt
            continue
        temp += bit
        if temp in reverse_code:
            decoded += reverse_code[temp]
            temp = ""
    return decoded

# ========  Baca file encoded dan codes ========
try:
    with open(encoded_path, "r", encoding="utf-8") as f:
        encoded_text = f.read()
    with open(codes_path, "r", encoding="utf-8") as f:
        codes = json.load(f)
except FileNotFoundError:
    print(" File encoded.txt atau codes.txt tidak ditemukan.")
    print(" Jalankan dulu huffman_encoder.py untuk membuatnya.")
    exit()

# ========  Decode proses ========
decoded_text = huffman_decode(encoded_text, codes)

# ========  Simpan hasil decode ========
with open(decoded_path, "w", encoding="utf-8") as f:
    f.write(decoded_text)

# ========  Tampilkan hasil ========
print("=== DECODE SELESAI ===")
print(f"📁 Folder output : {BASE_DIR}\n")
print(" decoded.txt → teks hasil dekompresi\n")
print(f"Panjang hasil decode : {len(decoded_text)} karakter\n")

print("Contoh hasil decode (awal):")
print(decoded_text[:300], "...\n")

# ========  Opsional: cek hasil dengan original.txt ========
original_path = os.path.join(BASE_DIR, "original.txt")
if os.path.exists(original_path):
    with open(original_path, "r", encoding="utf-8") as f:
        original = f.read()
    if decoded_text == original:
        print(" Hasil decode identik dengan teks asli (lossless).")
    else:
        print(" Ada perbedaan antara decoded dan teks asli.")
else:
    print(" File original.txt tidak ditemukan untuk perbandingan.")
