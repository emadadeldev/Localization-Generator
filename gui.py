import tkinter as tk
from tkinter import scrolledtext
import re


TAG_COLORS = {
    "~d~": "orange",
    "~z~": "red",
    "~lr": "gray"
}


def reverse_text(text):
    return text[::-1]


def update_preview(event=None):
    preview_text.config(state='normal')
    preview_text.delete(1.0, tk.END)

    text = input_text.get("1.0", tk.END).strip()

    
    text = reverse_text(text)

    
    prefix_pattern = re.compile(r'(~sl:|~d~|~z~)')
    match = prefix_pattern.search(text)
    if match:
        text_to_process = text[match.start():]
    else:
        text_to_process = text

    idx = 0
    while idx < len(text_to_process):
        tag_match = re.search(r'(~[a-z]{1,2}(:[^\~]*)?~)', text_to_process[idx:])
        if not tag_match:
            preview_text.insert(tk.END, text_to_process[idx:])
            break

        start_tag = idx + tag_match.start()
        end_tag = idx + tag_match.end()
        tag = tag_match.group(1)

        
        if start_tag > idx:
            preview_text.insert(tk.END, text_to_process[idx:start_tag])

        
        if tag.startswith("~d~"):
            end_d = text_to_process.find("~s~", end_tag)
            if end_d == -1:
                preview_text.insert(tk.END, text_to_process[end_tag:], "orange")
                break
            else:
                preview_text.insert(preview_text.index(tk.END), text_to_process[end_tag:end_d], "orange")
                idx = end_d + 3
                continue

        elif tag.startswith("~sl:"):
            preview_text.insert(tk.END, "\n")
            idx = end_tag
            continue

        elif tag.startswith("~z~") or tag.startswith("~lr"):
            idx = end_tag
            continue

        else:
            idx = end_tag

    preview_text.config(state='disabled')


def mirror_input(event=None):
    text = input_text.get("1.0", tk.END).rstrip("\n")
    reversed_text = reverse_text(text)
    input_text.delete("1.0", tk.END)
    input_text.insert("1.0", reversed_text)
    
    input_text.mark_set(tk.INSERT, tk.END)
    
    update_preview()


root = tk.Tk()
root.title("RDR2 Text Input & Preview")
root.geometry("900x450")

input_label = tk.Label(root, text="أدخل النص (سيتم عكسه تلقائيًا):")
input_label.pack()
input_text = scrolledtext.ScrolledText(root, height=7)
input_text.pack(fill=tk.X)
input_text.bind("<KeyRelease>", mirror_input)

preview_label = tk.Label(root, text="المعاينة (النص سليم):")
preview_label.pack()
preview_text = scrolledtext.ScrolledText(root, height=15, state='disabled', wrap=tk.WORD)
preview_text.pack(fill=tk.BOTH, expand=True)

preview_text.tag_configure("orange", foreground="orange")
preview_text.tag_configure("red", foreground="red")
preview_text.tag_configure("gray", foreground="gray")

root.mainloop()