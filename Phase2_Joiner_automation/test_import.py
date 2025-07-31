import csv

with open('users.csv', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row)  # should print each user as a dictionary
