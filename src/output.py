import csv
import datetime


def write_to_csv(parameter_dict):
    print('if no input, project will be named myReport by default')
    project_name = input('input report name: ')
    if project_name == '':
        project_name = 'myReport'
    current_time = datetime.datetime.now()
    file = open('output.csv', 'w')
    with open('output.csv', 'w', newline='') as csvfile:
        # writer = csv.writer(file)
        # writer.writerow(['project name', 'timestamp'])
        # writer.writerow([project_name, current_time])
        # # writer.writerow([project_name])

        # fieldnames = ['parameter', 'value']
        # dict_writer = csv.DictWriter(file, fieldnames=fieldnames)
        # dict_writer.writeheader()

        # for parameter in parameter_dict:
        #     dict_writer.writerow(
        #         {'parameter': parameter, 'value': parameter_dict[parameter]})
        # writer = csv.writer(file)
        writer = csv.writer(file)
        writer.writerow(['project name', 'timestamp'])
        writer.writerow([project_name, current_time])
        writer.writerow(['z', 'w', 'l', 'W', 'Lb'])
        writer.writerow([parameter_dict['z'], parameter_dict['w'], parameter_dict['l'],
                        parameter_dict['W'], parameter_dict['Lb']])
        writer.writerow(['Ph', '', '', 'gammaP'])
        writer.writerow(
            [parameter_dict['Ph'], round(parameter_dict['gammaP'], 3)])
        writer.writerow(['Zg', 'alpha', '', '', 'Kz'])
        writer.writerow(
            [parameter_dict['Zg'], parameter_dict['alpha'], '', '', '', round(parameter_dict['Kz'], 3)])
        writer.writerow(['elevation', '', '', '', 'Ke'])
        writer.writerow([parameter_dict['elevation'], '',
                        '', '', round(parameter_dict['Ke'], 3)])
        writer.writerow(['Kzt', 'Kd', 'v', 'qz'])
        writer.writerow([parameter_dict['Kzt'], parameter_dict['Kd'],
                        parameter_dict['v'], round(parameter_dict['qz'], 3)])
