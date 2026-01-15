import re
import arabic_reshaper

PREFIX_TAG_RE = re.compile(r'^(~[^~]+~)+')
BLOCK_RE = re.compile(r'~[^~]+~\([^()]*\)~[^~]+~')

def flip_ar(t: str) -> str:
    return arabic_reshaper.reshape(t)[::-1]

def process_line(text: str) -> str:
    prefix = ""
    m = PREFIX_TAG_RE.match(text)
    if m:
        prefix = m.group()
        text = text[len(prefix):]

    blocks = []
    i = 0

    for m in BLOCK_RE.finditer(text):
        if m.start() > i:
            blocks.append(("txt", text[i:m.start()]))
        blocks.append(("blk", m.group()))
        i = m.end()

    if i < len(text):
        blocks.append(("txt", text[i:]))

    out = []

    for kind, val in blocks:
        if kind == "blk":
            tag1, rest = val.split("(", 1)
            inner, tag2 = rest.rsplit(")", 1)
            out.append(f"{tag1}({flip_ar(inner)}){tag2}")
        else:
            out.append(flip_ar(val))

    return prefix + "".join(out[::-1])


with open("input.txt", "r", encoding="utf-8-sig", errors="ignore") as f:
    lines = f.readlines()

out_lines = []

for line in lines:
    line = line.rstrip("\n")

    if "=" in line:
        left, right = line.split("=", 1)
        out_lines.append(f"{left}={process_line(right)}\n")
    else:
        out_lines.append(line + "\n")

with open("localization.gxt2", "w", encoding="utf-8") as f:
    f.writelines(out_lines)

print("Done")
