import re
import arabic_reshaper
from bidi.algorithm import get_display

# الأنماط المدعومة
pattern_space_id = re.compile(r'^(.*?)[ \t]+(0x[0-9A-F]{8})$')
pattern_text_id  = re.compile(r'^(.*)=(0x[0-9A-F]{8})$')
pattern_id_text  = re.compile(r'^(0x[0-9A-F]{8})=(.*)$')

def reshape_arabic(text: str) -> str:
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

with open("input.txt", "r", encoding="utf-8-sig") as f:
    lines = f.readlines()

out_lines = []

for line in lines:
    line = line.strip()

    # 1) احذف السطور الفاضية
    if not line:
        continue

    text = None
    hex_id = None

    m = pattern_space_id.match(line)
    if m:
        text, hex_id = m.group(1), m.group(2)
    else:
        m = pattern_text_id.match(line)
        if m:
            text, hex_id = m.group(1), m.group(2)
        else:
            m = pattern_id_text.match(line)
            if m:
                hex_id, text = m.group(1), m.group(2)

    # لو السطر مش مفهوم سيبه زي ما هو
    if text is None or hex_id is None:
        continue

    text = text.strip()

    # 2) احذف السطور اللي ID= بس (من غير نص)
    if not text:
        continue

    visual_text = reshape_arabic(text)
    out_lines.append(f"{hex_id}={visual_text}\n")

with open("output.txt", "w", encoding="utf-8") as f:
    f.writelines(out_lines)

print("✔ تم حذف السطور الفارغة + السطور بدون نص + عكس النصوص العربية")
