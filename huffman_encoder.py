# ==============================================================
# Program   : Huffman Encoder 
# Author    : Rahmatul Zikri
# ==============================================================

import os
import json
from heapq import heappush, heappop
from collections import Counter, namedtuple

# ======== Path folder yang sama ========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ======== Masukkan teks ========
text = """
What’s New in the Seventh Edition
 In this revision, we increased the discussions of program examples early in the book, added more sup
plemental review questions and key terms, introduced 64-bit programming, and reduced our depen
dence on the book’s subroutine library. To be more specific, here are the details:
 • Early chapters now include short sections that feature 64-bit CPU architecture and program
ming, and we have created a 64-bit version of the book’s subroutine library named Irvine64.
 • Many of the review questions and exercises have been modified, replaced, and moved from
 the middle of the chapter to the end of chapters, and divided into two sections: (1) Short
 answer questions, and (2) Algorithm workbench exercises. The latter exercises require the
 student to write a short amount of code to accomplish a goal.
 • Each chapter now has a Key Terms section, listing new terms and concepts, as well as new
 MASM directives and Intel instructions.
 • New programming exercises have been added, others removed, and a few existing exercises
 were modified.
 • There is far less dependency on the author's subroutine libraries in this edition. Students are
 encouraged to call system functions themselves and use the Visual Studio debugger to step
 through the programs. The Irvine32 and Irvine64 libraries are available to help students han
dle input/output, but their use is not required.
 • New tutorial videos covering essential content topics have been created by the author and
 added to the Pearson website.
 This book is still focused on its primary goal, to teach students how to write and debug programs at
 the machine level. It will never replace a complete book on computer architecture, but it does give
 students the first-hand experience of writing software in an environment that teaches them how a
 computer works. Our premise is that students retain knowledge better when theory is combined with
 experience. In an engineering course, students construct prototypes; in a computer architecture
 course, students should write machine-level programs. In both cases, they have a memorable experi
ence that gives them the confidence to work in any OS/machine-oriented environment.
 Protected mode programming is entirely the focus of the printed chapters (1 through 13). As such,
 students will create 32-bit and 64-bit programs that run under the most recent versions of Microsoft
 Windows. The remaining four chapters cover 16-bit programming, and are supplied in electronic
 form.  These chapters cover BIOS programming, MS-DOS services, keyboard and mouse input,
 video  programming, and graphics. One chapter covers disk storage fundamentals. Another chapter
 covers advanced DOS programming techniques. 
Subroutine Libraries 
We supply three versions of the subroutine library that students use for
 basic input/output, simulations, timing, and other useful tasks. The Irvine32 and Irvine64 libraries run
 in protected mode. The 16-bit version (Irvine16.lib) runs in real-address mode and is used only by
 Chapters 14 through 17. Full source code for the libraries is supplied on the companion website. The
 link libraries are available only for convenience, not to prevent students from learning how to pro
gram input–output themselves. 
"""

# ======== Kelas Node & Leaf ========
class Node(namedtuple("Node", ["left", "right"])):
    def walk(self, code, acc):
        self.left.walk(code, acc + "0")
        self.right.walk(code, acc + "1")

class Leaf(namedtuple("Leaf", ["char"])):
    def walk(self, code, acc):
        code[self.char] = acc or "0"

# ======== Fungsi Huffman ========
def build_huffman_code(s):
    freq = Counter(s)
    heap = []
    for ch, fr in freq.items():
        heappush(heap, (fr, len(heap), Leaf(ch)))
    count = len(heap)
    while len(heap) > 1:
        f1, _c1, left = heappop(heap)
        f2, _c2, right = heappop(heap)
        heappush(heap, (f1 + f2, count, Node(left, right)))
        count += 1
    code = {}
    if heap:
        [(_freq, _count, root)] = heap
        root.walk(code, "")
    return code

def huffman_encode(text, code):
    return ''.join(code[ch] for ch in text)

# ======== Jalankan proses ========
codes = build_huffman_code(text)
encoded_text = huffman_encode(text, codes)

# ======== Format agar hasil biner tidak menyamping ========
WRAP = 100  # ubah sesuai keinginan (misal 64/128)
wrapped_encoded = '\n'.join(encoded_text[i:i+WRAP] for i in range(0, len(encoded_text), WRAP))

# ======== Simpan hasil ========
encoded_path  = os.path.join(BASE_DIR, "encoded.txt")
codes_path    = os.path.join(BASE_DIR, "codes.txt")
original_path = os.path.join(BASE_DIR, "original.txt")

with open(encoded_path, "w", encoding="utf-8") as f:
    f.write(wrapped_encoded)
with open(codes_path, "w", encoding="utf-8") as f:
    json.dump(codes, f, ensure_ascii=False, indent=2)
with open(original_path, "w", encoding="utf-8") as f:
    f.write(text)

# ======== Output ========
print("=== ENCODING SELESAI ===")
print(f"Jumlah karakter asli : {len(text)}")
print(f"Panjang hasil encode : {len(encoded_text)} bit\n")
print(f"📁 File tersimpan di folder:\n{BASE_DIR}\n")
print("encoded.txt   → hasil encode ")
print("codes.txt     → tabel kode Huffman")
print("original.txt  → teks asli\n")
print("Contoh hasil encode:\n", wrapped_encoded.splitlines()[0][:100], "...")
