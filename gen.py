import re
import arabic_reshaper

# ================= REGEX =================
PREFIX_TAG_RE = re.compile(r'^(~[^~]+~)+')          # ~z~ ~sl:x:y~
INLINE_TAG_RE = re.compile(r'(~[^~]+~)')           # أي tag بين ~~
BLOCK_RE = re.compile(r'~[^~]+~\([^()]*\)~[^~]+~')  # ~d~(...)~s~
PAREN_RE = re.compile(r'\([^()]*\)')                # (text)

# ================= HELPERS =================
def flip_ar(text: str) -> str:
    return arabic_reshaper.reshape(text)[::-1]

def insert_newlines_smart(text: str, max_len: int = 50) -> str:
    if len(text) <= max_len:
        return text
    
    mid = len(text) // 2
    cut = text.rfind(" ", 0, mid)
    if cut == -1:
        cut = mid
    return text[:cut] + "~n~" + text[cut:].lstrip()

def process_segment(text: str, add_newlines=True) -> str:
    tokens = []
    i = 0

    for m in BLOCK_RE.finditer(text):
        if m.start() > i:
            segment = text[i:m.start()]
            if add_newlines:
                segment = insert_newlines_smart(segment)
            tokens.append(segment)
        tokens.append(m.group())
        i = m.end()

    if i < len(text):
        segment = text[i:]
        if add_newlines:
            segment = insert_newlines_smart(segment)
        tokens.append(segment)

    final = []
    for tok in tokens:
        if BLOCK_RE.fullmatch(tok):
            tag1, rest = tok.split("(", 1)
            inner, tag2 = rest.rsplit(")", 1)
            final.append(f"{tag1}({flip_ar(inner)}){tag2}")
        else:
            final.append(flip_ar(tok))

    return "".join(final)

def process_line(text: str) -> str:
    add_newlines = "~sl:" not in text

    prefix = ""
    m = PREFIX_TAG_RE.match(text)
    if m:
        prefix = m.group()
        text = text[len(prefix):]

    parts = INLINE_TAG_RE.split(text)
    out = []

    for p in parts:
        if not p:
            continue
        if INLINE_TAG_RE.fullmatch(p):
            out.append(p)
        else:
            out.append(process_segment(p, add_newlines=add_newlines))

    return prefix + "".join(out)

# ================= FILE IO =================
with open("input.txt", "r", encoding="utf-8-sig", errors="ignore") as f:
    lines = f.readlines()

out_lines = []

for line in lines:
    line = line.rstrip("\n")
    if not line.strip():
        continue

    if "=" in line:
        left, right = line.split("=", 1)
        if not right.strip() or all(t.startswith("~") and t.endswith("~") for t in right.split() if t):
            continue
        out_lines.append(f"{left}={process_line(right)}\n")
    else:
        out_lines.append(line + "\n")

with open("localization.gxt2", "w", encoding="utf-8") as f:
    f.writelines(out_lines)

print("Done")
