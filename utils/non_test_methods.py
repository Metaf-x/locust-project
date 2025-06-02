import csv

def open_csv_field(filepath=str):
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)