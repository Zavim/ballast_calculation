import csv
import datetime


def write_to_csv(parameter_dict, array):
    print('if no input, project will be named myReport by default')
    project_name = input('input report name: ')
    if project_name == '':
        project_name = 'myReport'
    current_time = datetime.datetime.now()
    current_time = current_time.strftime(
        '%Y-%m-%d, %H:%M')  # remove millisecs from time
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
        writer.writerow([''])
        writer.writerow(['z', 'w', 'l', 'W', 'Lb'])
        writer.writerow([parameter_dict['z'], parameter_dict['w'], parameter_dict['l'],
                        parameter_dict['W'], parameter_dict['Lb']])
        writer.writerow([''])
        writer.writerow(['Ph', 'gammaP'])
        writer.writerow(
            [parameter_dict['Ph'], round(parameter_dict['gammaP'], 2)])
        writer.writerow([''])
        writer.writerow(['Zg', 'alpha', 'Kz'])
        writer.writerow(
            [parameter_dict['Zg'], parameter_dict['alpha'], round(parameter_dict['Kz'], 2)])
        writer.writerow([''])
        writer.writerow(['elevation', 'Ke'])
        writer.writerow([parameter_dict['elevation'],
                        round(parameter_dict['Ke'], 2)])
        writer.writerow([''])
        writer.writerow(['Kzt', 'Kd', 'v', 'qz'])
        writer.writerow([parameter_dict['Kzt'], parameter_dict['Kd'],
                        parameter_dict['v'], round(parameter_dict['qz'], 2)])
        writer.writerow([''])
        writer.writerow(['LSFc', 'LSFe', 'LSFi'])
        writer.writerow([''])
        writer.writerow(['panel length', 'panel width', 'Aref'])
        writer.writerow(
            [array[0].length, array[0].width, array[0].Aref])
        writer.writerow([''])
        writer.writerow(['panel index', 'panel coords',
                        'zones', 'intersection area', 'An', 'GCL'])

        for panel in array:
            zones_after_rounding = []
            for zone in panel.zones:
                zones_after_rounding.append(round(panel.zones[zone], 2))
            writer.writerow(
                [panel.identity, list(panel.polygon.exterior.coords[:-1]), list(panel.zones.keys()), zones_after_rounding, round(panel.An, 2), round(panel.gcl, 2)])
            zones_after_rounding = []
            # print(zones_after_rounding)
