import re
import arabic_reshaper

arabic_re = re.compile(r'[\u0600-\u06FF\sً-ْ"”،]+')

def flip_text(text: str) -> str:
    reshaped = arabic_reshaper.reshape(text)
    return reshaped[::-1]

tag_re = re.compile(r'(~[^~]+~|\([^)]+\))')

def process_line(line: str) -> str:
    parts = tag_re.split(line) 
    result = []

    for part in parts:
        if tag_re.fullmatch(part):
            result.append(part)  
        elif arabic_re.search(part):
            result.append(flip_text(part))  
        else:
            result.append(part)  
    return "".join(result)


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
        right = right.lstrip()

        right = process_line(right)
        out_lines.append(f"{left}={right}\n")
    else:
        out_lines.append(line + "\n")

with open("localization.gxt2", "w", encoding="utf-8") as f:
    f.writelines(out_lines)

print("Done")