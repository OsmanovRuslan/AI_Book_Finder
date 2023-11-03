import csv

input_file = 'book_new.csv'
output_file = 'books.csv'

with open(input_file, 'r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    headers = reader.fieldnames

    rows_to_keep = []
    for row in reader:
        if len(row['description'].split(" ")) >= 25:
            rows_to_keep.append(row)

with open(output_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows_to_keep)