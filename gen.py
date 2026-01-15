import re
import arabic_reshaper

arabic_re = re.compile(r'[\u0600-\u06FF0-9]')
tag_or_paren_re = re.compile(r'(~[^~]+~|\([^()]*\))')

def flip_arabic_text(text: str) -> str:
    reshaped = arabic_reshaper.reshape(text)
    return reshaped[::-1]

def process_part(part: str) -> str:
    if part.startswith("~") and part.endswith("~"):
        return part

    if part.startswith("(") and part.endswith(")"):
        inner = part[1:-1]
        if arabic_re.search(inner):
            inner = flip_arabic_text(inner)
        return f"({inner})"

    if arabic_re.search(part):
        return flip_arabic_text(part)

    return part

def process_line(text: str) -> str:
    parts = tag_or_paren_re.split(text)
    return "".join(process_part(p) for p in parts if p)


with open("input.txt", "r", encoding="utf-8-sig", errors="ignore") as f:
    lines = f.readlines()

out_lines = []

for line in lines:
    line = line.rstrip("\n")

    if "=" in line:
        left, right = line.split("=", 1)
        right = process_line(right)
        out_lines.append(f"{left}={right}\n")
    else:
        out_lines.append(line + "\n")

with open("localization.gxt2", "w", encoding="utf-8") as f:
    f.writelines(out_lines)

print("Done")
