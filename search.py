import os

SEARCH_TEXT = "Bill, Micah and Sean are meeting the Grays over at the saloon about a job."
FOLDER_PATH = r"E:\Github\Localization-Generator\org"

for root, _, files in os.walk(FOLDER_PATH):
    for file in files:
        if file.lower().endswith(".txt"):
            file_path = os.path.join(root, file)

            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line_number, line in enumerate(f, start=1):
                        if SEARCH_TEXT in line:
                            print(f"[FOUND] {file_path}")
                            print(f"  Line {line_number}: {line.strip()}\n")

            except Exception as e:
                print(f"[ERROR] {file_path} -> {e}")