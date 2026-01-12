import re
import arabic_reshaper
from bidi.algorithm import get_display

arabic_re = re.compile(r'[\u0600-\u06FF]')
pattern_hex = re.compile(r'0x[0-9A-F]{8}')

def reshape_arabic(text: str) -> str:
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

with open("input.txt", "r", encoding="utf-8-sig", errors="ignore") as f:
    lines = f.readlines()

out_lines = []

for line in lines:
    line = line.strip()
    if not line:
        continue  

    if "=" in line:
        left, right = line.split("=", 1)
        left = left.strip()
        right = right.lstrip(" \t")  
        if not right:
            continue  
        if arabic_re.search(right):
            right = reshape_arabic(right)
        out_lines.append(f"{left}={right}\n")
    else:
        out_lines.append(line + "\n")

with open("localization.gxt2", "w", encoding="utf-8") as f:
    f.writelines(out_lines)

print("Done")