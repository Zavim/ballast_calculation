import csv
import sys
import datetime


def write_to_csv(parameter_dict):
    print('if no input, project will be named myReport by default')
    project_name = input('input report name: ')
    if project_name == '':
        project_name = 'myReport'
    current_time = datetime.datetime.now()
    file = open('output.csv', 'w')
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(file)
        writer.writerow([current_time])
        writer.writerow([project_name])

        fieldnames = ['parameter', 'value']
        dict_writer = csv.DictWriter(file, fieldnames=fieldnames)
        dict_writer.writeheader()

        for parameter in parameter_dict:
            dict_writer.writerow(
                {'parameter': parameter, 'value': parameter_dict[parameter]})
