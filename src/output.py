import csv
import datetime


def write_parameters(parameter_dict, array):
    print('if no input, project will be named myReport by default')
    report_name = input('input report name: ')
    if report_name == '':
        report_name = 'myReport'
    report_name += '.csv'
    file = open(report_name, 'w')
    current_time = datetime.datetime.now()
    current_time = current_time.strftime(
        '%Y-%m-%d, %H:%M')  # remove millisecs from time
    with open(report_name, 'w', newline='') as csvfile:
        writer = csv.writer(file)
        # writer.writerow(['report name', 'timestamp', 'z', 'w', 'l', 'W', 'Lb', 'h2', 'Ph', 'gammaP', 'Zg', 'alpha', 'Kz', 'elevation', 'Ke', 'Kzt', 'Kd', 'v', 'qz', 'LSFc', 'LSFe', 'LSFi', 'panel length', 'panel width', 'Aref', 'array rows', 'array columns', 'panel index', 'panel coords', 'panel class',
        #                 'zones', 'intersection area', 'vortex zones', 'An', 'GCL', 'GCS', 'gamma_e'])
        # writer.writerow([report_name[:-4], current_time, parameter_dict['z'], parameter_dict['w'], parameter_dict['l'],
        #                 parameter_dict['W'], parameter_dict['Lb'], parameter_dict['h2'], parameter_dict['Ph'], round(
        #                     parameter_dict['gammaP'], 2), parameter_dict['Zg'], parameter_dict['alpha'], round(parameter_dict['Kz'], 2), parameter_dict['elevation'],
        #                 round(
        #                     parameter_dict['Ke'], 2), parameter_dict['Kzt'], parameter_dict['Kd'],
        #                 parameter_dict['v'], round(parameter_dict['qz'], 2), 0, 0, 0, array[0].length, array[0].width, array[0].Aref, array[-1].index[0]+1, array[-1].index[1]+1])

    writer.writerow([''])
    writer.writerow(['z', 'w', 'l', 'W', 'Lb'])
    writer.writerow([parameter_dict['z'], parameter_dict['w'], parameter_dict['l'],
                    parameter_dict['W'], parameter_dict['Lb']])
    writer.writerow([''])
    writer.writerow(['h2'])
    writer.writerow([parameter_dict['h2']])
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
    writer.writerow(
        [parameter_dict['LSFc'], parameter_dict['LSFe'], parameter_dict['LSFi']])
    writer.writerow([''])
    writer.writerow(['panel length', 'panel width', 'Aref'])
    writer.writerow([''])
    writer.writerow(
        [array.panel_list[0].length, array.panel_list[0].width, array.panel_list[0].length * array.panel_list[0].width])
    # all panels will have the same length, width, and area so this line just
    # picks the first panel from the array to get these values
    writer.writerow([''])
    return report_name, file, writer


def write_panels(report_name, file, writer, parameter_dict, array):
    panel_parameters = {}
    writer.writerow(['array rows', 'array columns', 'array total'])
    writer.writerow([''])
    writer.writerow([array.rows, array.columns, array.array_total])
    writer.writerow([''])
    writer.writerow(['panel index', 'panel coords', 'panel class',
                    'zones', 'vortex zones', 'gammaE', 'qz*gammaP*gammaE', 'LSF', 'AtribL', 'AnL', 'GCL', 'forceL', 'AtribS', 'AnS', 'GCS', 'forceS', 'maxForce'])
    writer.writerow([''])

    for panel in array.panel_list:
        for zone in panel.zones:
            panel.zones[zone] = round(panel.zones[zone], 2)
        panel_parameters['panel index'] = panel.index
        panel_parameters['panel coords'] = list(
            panel.polygon.exterior.coords[:-1])
        panel_parameters['panel class'] = panel.panel_class
        writer.writerow([panel.index, list(panel.polygon.exterior.coords[:-1]), panel.panel_class, panel.zones,
                        panel.vortex_zones, panel.gamma_e, round(parameter_dict['qz'] * parameter_dict['gammaP']*panel.gamma_e, 1), panel.load_share_factor, round(panel.AtribL, 2), round(panel.AnL, 2), round(panel.gcl, 2), round(panel.forceL), round(panel.AtribS, 2), round(panel.AnS), round(panel.gcs, 2), round(panel.forceS), round(min(panel.forceS, panel.forceL))])
        # list(panel.zones.keys()), zones_after_rounding, panel.vortex_zones, round(panel.An, 2), round(panel.gcl, 2), round(panel.gcs, 2), round(panel.gamma_e, 2)])
