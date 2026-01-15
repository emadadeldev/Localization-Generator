import re
import arabic_reshaper

# ================= REGEX =================

PREFIX_TAG_RE = re.compile(r'^(~[^~]+~)+')          # ~z~ ~sl:x:y~
INLINE_TAG_RE = re.compile(r'(~rp~|~sl:~)')         # fixed inline tags
BLOCK_RE = re.compile(r'~[^~]+~\([^()]*\)~[^~]+~')  # ~d~(...)~s~
PAREN_RE = re.compile(r'\([^()]*\)')                # (text)


# ================= HELPERS =================

def flip_ar(text: str) -> str:
    return arabic_reshaper.reshape(text)[::-1]


def process_segment(text: str) -> str:
    """
    Processes text safely:
    - parentheses are atomic
    - spaces preserved
    - order reversed correctly
    """
    tokens = []
    i = 0

    # 1) protect ~d~(...)~s~
    for m in BLOCK_RE.finditer(text):
        if m.start() > i:
            tokens.append(("txt", text[i:m.start()]))
        tokens.append(("blk", m.group()))
        i = m.end()

    if i < len(text):
        tokens.append(("txt", text[i:]))

    final = []

    for kind, val in tokens:
        if kind == "blk":
            tag1, rest = val.split("(", 1)
            inner, tag2 = rest.rsplit(")", 1)
            final.append(("blk", f"{tag1}({flip_ar(inner)}){tag2}"))
        else:
            # split text further by parentheses
            pos = 0
            for pm in PAREN_RE.finditer(val):
                if pm.start() > pos:
                    final.append(("txt", flip_ar(val[pos:pm.start()])))
                inner = pm.group()[1:-1]
                final.append(("par", f"({flip_ar(inner)})"))
                pos = pm.end()
            if pos < len(val):
                final.append(("txt", flip_ar(val[pos:])))

    # reverse order BUT keep tokens intact
    return "".join(v for _, v in final[::-1])


def process_line(text: str) -> str:
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
            out.append(process_segment(p))

    return prefix + "".join(out)


# ================= FILE IO =================

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
