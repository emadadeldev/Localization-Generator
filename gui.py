import tkinter as tk
from tkinter import scrolledtext
import re

# ======  tag ======
TAG_COLORS = {
    "~d~": "orange",  
    "~z~": "red",     
    "~lr": "gray"    
}

# ====== Preview ======
def update_preview(event=None):
    preview_text.config(state='normal')
    preview_text.delete(1.0, tk.END)
    
    text = input_text.get("1.0", tk.END).strip()

    prefix_pattern = re.compile(r'(~sl:|~d~)')
    match = prefix_pattern.search(text)
    if match:
        text = text[match.start():]
    
    idx = 0
    while idx < len(text):
        tag_match = re.search(r'(~[a-z]{1,2}(:[^\~]*)?~)', text[idx:])
        if not tag_match:
            preview_text.insert(tk.END, text[idx:])
            break

        start_tag = idx + tag_match.start()
        end_tag = idx + tag_match.end()
        tag = tag_match.group(1)

        preview_text.insert(tk.END, text[idx:start_tag])

        if tag.startswith("~d~"):
            end_d = text.find("~s~", end_tag)
            if end_d == -1:
                colored_text = text[end_tag:]
                preview_text.insert(tk.END, colored_text, "orange")
                break
            else:
                colored_text = text[end_tag:end_d]
                preview_text.insert(tk.END, colored_text, "orange")
                idx = end_d + 3
                continue

        elif tag.startswith("~sl:"):
            preview_text.insert(tk.END, "\n")
            idx = end_tag
            continue

        elif tag.startswith("~z~"):
            idx = end_tag
            continue

        elif tag.startswith("~lr"):
            idx = end_tag
            continue

        else:
            idx = end_tag

    preview_text.config(state='disabled')

root = tk.Tk()
root.title("RDR2 Text Preview")
root.geometry("900x450")

input_label = tk.Label(root, text="أدخل النص هنا:")
input_label.pack()
input_text = scrolledtext.ScrolledText(root, height=7)
input_text.pack(fill=tk.X)
input_text.bind("<KeyRelease>", update_preview)

preview_label = tk.Label(root, text="المعاينة (كما في RDR2):")
preview_label.pack()
preview_text = scrolledtext.ScrolledText(root, height=15, state='disabled', wrap=tk.WORD)
preview_text.pack(fill=tk.BOTH, expand=True)

preview_text.tag_configure("orange", foreground="orange")
preview_text.tag_configure("red", foreground="red")
preview_text.tag_configure("gray", foreground="gray")

root.mainloop()
