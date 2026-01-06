import csv

input_file = "default.csv"
output_file = "edit.csv"

with open(input_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    with open(output_file, "w", encoding="utf-8") as f_out:
        for row in reader:
            if len(row) < 4:
                continue
            id_ = row[0].strip()
            ar_text = row[3].strip()
            reversed_text = ar_text[::-1]
            f_out.write(f"{id_}={reversed_text}\n")

print(output_file)