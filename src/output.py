import csv
import sys


file = open('output.csv', 'w')
with open('output.csv', 'w', newline='') as csvfile:
    fieldnames = ['input', 'value']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'input': 'test', 'value': 'Don'})
    writer.writerow({'input': 'test', 'value': 'Saba'})
    writer.writerow({'input': 'test', 'value': 'Zavier'})
