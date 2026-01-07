import re
import arabic_reshaper
from bidi.algorithm import get_display

pattern_id_text = re.compile(r'^(0x[0-9A-F]{8})=(.*)$')
pattern_text_id = re.compile(r'^(.*)=(0x[0-9A-F]{8})$')

def reshape_arabic(text: str) -> str:
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

with open("input.txt", "r", encoding="utf-8-sig") as f:
    lines = f.readlines()

out_lines = []

for line in lines:
    line = line.rstrip("\n")

    m1 = pattern_id_text.match(line)
    m2 = pattern_text_id.match(line)

    if m1:
        hex_id = m1.group(1)
        text = m1.group(2)

    elif m2:
        hex_id = m2.group(2)
        text = m2.group(1)

    else:
        out_lines.append(line + "\n")
        continue

    visual_text = reshape_arabic(text)
    out_lines.append(f"{hex_id}={visual_text}\n")

with open("output.txt", "w", encoding="utf-8") as f:
    f.writelines(out_lines)

print("Done")
