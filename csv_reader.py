import csv

def read_column_from_csv(file_path, column_name):
    values = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            values.append(float((row[column_name])))
    return values