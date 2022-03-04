from shapely.geometry import Polygon


class Building:
    def __init__(self, coordinates, length, width, height, polygon):
        self.coordinates = coordinates
        self.length = length
        self.width = width
        self.height = height
        self.polygon = polygon


def build_polygons(coordinates):
    polygon = Polygon(coordinates)
    return polygon


def calculate_building_coordinates(preset='', building_width=0, building_length=0, building_height=0):
    if preset:
        if preset == 'default':
            coordinates = [[0.0, 0.0], [0.0, 500.0],
                           [500.0, 500.0], [500.0, 0.0]]
            building_height = 20.0
            return coordinates, building_height

        if preset == 'alberta':
            coordinates = [[0.0, 0.0], [0.0, 600.0],
                           [2057.0, 600.0], [2057.0, 0.0]]
            building_height = 40.0
            return coordinates, building_height

        if preset == 'anisa':
            coordinates = [[0.0, 0.0], [0.0, 500.0],
                           [500.0, 500.0], [500.0, 0.0]]
            building_height = 33.0
            return coordinates, building_height

        if preset == 'rect':
            coordinates = [[0.0, 0.0], [0.0, 500.0],
                           [1000.0, 500.0], [1000.0, 0.0]]
            building_height = 33.0
            return coordinates, building_height

    coordinates = [[0.0, 0.0], [0.0, building_length],
                   [building_width, building_length], [building_width, 0.0]]
    building_height = building_height
    return coordinates, building_height


def calculate_vortex_zones(building):
    building_origin_x = building.coordinates[0][0]
    building_origin_y = building.coordinates[0][1]
    building_max_x = building.coordinates[2][1]
    building_max_y = building.coordinates[2][0]

    vortex_formulas_length = {
        'VNE-E': {1: [building_origin_x, building_origin_y], 2: [building_origin_x, building_max_y], 3: [building_max_x, building_max_y]},
        'VNE-N': {1: [(building_max_x-building_max_y), building_origin_y], 2: [building_max_x, building_max_y], 3: [building_max_x, building_origin_y]},
        'VNW-W': {1: [building_origin_x, building_max_y], 2: [building_max_x, building_max_y], 3: [building_max_x, building_origin_y]},
        'VNW-N': {1: [building_origin_x, building_origin_y], 2: [building_origin_x, building_max_y], 3: [building_max_y, building_origin_x]},
        'VSW-W': {1: [building_origin_x, building_origin_y], 2: [building_origin_x, building_max_y], 3: [(building_max_x-building_max_y), building_origin_y]},
        'VSW-S': {1: [(building_max_x-building_max_y), building_origin_y], 2: [building_max_x, building_max_y], 3: [building_max_x, building_origin_y]},
        'VSE-E': {1: [building_origin_x, building_origin_y], 2: [building_origin_x, building_max_y], 3: [(building_max_x-building_max_y), building_max_y]},
        'VSE-S': {1: [(building_max_x-building_max_y), building_max_y], 2: [building_max_x, building_max_y], 3: [building_max_x, building_origin_y]}
    }

    vortex_formulas_width = {
        'VNE-E': {1: [building_origin_x, building_origin_y], 2: [building_origin_x, building_max_y], 3: [building_max_x, building_max_y]},
        'VNE-N': {1: [(building_max_x-building_max_y), building_origin_y], 2: [building_max_x, building_max_y], 3: [building_max_x, building_origin_y]},
        'VNW-W': {1: [building_origin_x, building_max_y], 2: [building_max_x, building_max_y], 3: [building_max_x, building_origin_y]},
        'VNW-N': {1: [building_origin_x, building_origin_y], 2: [building_origin_x, building_max_y], 3: [building_max_y, building_origin_x]},
        'VSW-W': {1: [building_origin_x, building_origin_y], 2: [building_origin_x, building_max_y], 3: [(building_max_x-building_max_y), building_origin_y]},
        'VSW-S': {1: [(building_max_x-building_max_y), building_origin_y], 2: [building_max_x, building_max_y], 3: [building_max_x, building_origin_y]},
        'VSE-E': {1: [building_origin_x, building_origin_y], 2: [building_origin_x, building_max_y], 3: [(building_max_x-building_max_y), building_max_y]},
        'VSE-S': {1: [(building_max_x-building_max_y), building_max_y], 2: [building_max_x, building_max_y], 3: [building_max_x, building_origin_y]}
    }
    vortex_zones = {}
    if building.length >= building.width:
        for key in vortex_formulas_length:
            vortex_zones[key] = list(
                iter(vortex_formulas_length[key].values()))
            vortex_zones[key] = build_polygons(vortex_zones[key])
        return vortex_zones
    else:
        for key in vortex_formulas_length:
            vortex_zones[key] = list(iter(vortex_formulas_width[key].values()))
            vortex_zones[key] = build_polygons(vortex_zones[key])
        return vortex_zones


def calculate_zones(building):
    W = max(building.length, building.width)
    z = building.height
    Lb = min(z, 0.4 * (W * z) ** 1/2)
    building_origin_x = building.coordinates[0][0]
    building_origin_y = building.coordinates[0][1]
    building_max_x = building.coordinates[2][0]
    building_max_y = building.coordinates[2][1]
#     rename these to direction+zone, eg EA2
    formulas = {'3A1': {1: [building_max_x, building_max_y],
                        2: [building_max_x, building_max_y-2*Lb],
                        3: [building_max_x-2*Lb, building_max_y-2*Lb],
                        4: [building_max_x-0.5*Lb, building_max_y]},
                '3A2': {1: [building_max_x-0.5*Lb, building_max_y],
                        2: [building_max_x-2*Lb, building_max_y-2*Lb],
                        3: [building_max_x-4*Lb, building_max_y-2*Lb],
                        4: [building_max_x-4*Lb, building_max_y]},
                '3B': {1: [building_max_x, building_max_y-2*Lb],
                       2: [building_max_x, building_max_y-4*Lb],
                       3: [building_max_x-2*Lb, building_max_y-4*Lb],
                       4: [building_max_x-2*Lb, building_max_y-2*Lb]},
                '3C': {1: [building_max_x-6*Lb, building_max_y],
                       2: [building_max_x-4*Lb, building_max_y],
                       3: [building_max_x-4*Lb, building_max_y-2*Lb],
                       4: [building_max_x-2*Lb, building_max_y-2*Lb],
                       5: [building_max_x-2*Lb, building_max_y-4*Lb],
                       6: [building_max_x, building_max_y-4*Lb],
                       7: [building_max_x, building_max_y-6*Lb],
                       8: [building_max_x-4*Lb, building_max_y-6*Lb],
                       9: [building_max_x-4*Lb, building_max_y-4*Lb],
                       10: [building_max_x-6*Lb, building_max_y-4*Lb]},
                '4E': {1: [building_max_x-5*Lb, building_origin_y+2*Lb],
                       2: [building_max_x-5*Lb, building_origin_y],
                       3: [building_origin_x, building_origin_y],
                       4: [building_origin_x, building_origin_y+3*Lb],
                       5: [building_max_x-7*Lb, building_origin_y+3*Lb],
                       6: [building_max_x-7*Lb, building_origin_y+2*Lb]},
                '4F1': {1: [building_max_x, building_origin_y],
                        2: [building_max_x-2*Lb, building_origin_y],
                        3: [building_max_x-2*Lb, building_origin_y+Lb],
                        4: [building_max_x, building_origin_y+0.5*Lb]},
                '4F2': {1: [building_max_x-2*Lb, building_origin_y+2*Lb],
                        2: [building_max_x-2*Lb, building_origin_y],
                        3: [building_max_x-5*Lb, building_origin_y],
                        4: [building_max_x-5*Lb, building_origin_y+2*Lb]},
                '4G1': {1: [building_max_x, building_origin_y+3*Lb],
                        2: [building_max_x, building_origin_y+0.5*Lb],
                        3: [building_max_x-2*Lb, building_origin_y+Lb],
                        4: [building_max_x-2*Lb, building_origin_y+3*Lb]},
                '4G2': {1: [building_max_x-2*Lb, building_origin_y+6*Lb],
                        2: [building_max_x, building_origin_y+6*Lb],
                        3: [building_max_x, building_origin_y+3*Lb],
                        4: [building_max_x-2*Lb, building_origin_y+3*Lb],
                        5: [building_max_x-2*Lb, building_origin_y+2*Lb],
                        6: [building_max_x-7*Lb, building_origin_y+2*Lb],
                        7: [building_max_x-7*Lb, building_origin_y+4*Lb],
                        8: [building_max_x-2*Lb, building_origin_y+4*Lb]},
                '2A1': {1: [building_origin_x, building_max_y],
                        2: [building_origin_x+0.5*Lb, building_max_y],
                        3: [building_origin_x+2*Lb, building_max_y-2*Lb],
                        4: [building_origin_x, building_max_y-2*Lb]},
                '2A2': {1: [building_origin_x+0.5*Lb, building_max_y],
                        2: [building_origin_x+4*Lb, building_max_y],
                        3: [building_origin_x+4*Lb, building_max_y-2*Lb],
                        4: [building_origin_x+2*Lb, building_max_y-2*Lb]},
                '2B': {1: [building_origin_x, building_max_y-2*Lb],
                       2: [building_origin_x+2*Lb, building_max_y-2*Lb],
                       3: [building_origin_x+2*Lb, building_max_y-4*Lb],
                       4: [building_origin_x, building_max_y-4*Lb]},
                '2C': {1: [building_origin_x+4*Lb, building_max_y],
                       2: [building_origin_x+6*Lb, building_max_y],
                       3: [building_origin_x+6*Lb, building_max_y-4*Lb],
                       4: [building_origin_x+4*Lb, building_max_y-4*Lb],
                       5: [building_origin_x+4*Lb, building_max_y-6*Lb],
                       6: [building_origin_x, building_max_y-6*Lb],
                       7: [building_origin_x, building_max_y-4*Lb],
                       8: [building_origin_x+2*Lb, building_max_y-4*Lb],
                       9: [building_origin_x+2*Lb, building_max_y-2*Lb],
                       10: [building_origin_x+4*Lb, building_max_y-2*Lb]},
                '1E': {1: [building_origin_x+5*Lb, building_origin_y],
                       2: [building_origin_x+5*Lb, building_origin_y+2*Lb],
                       3: [building_origin_x+7*Lb, building_origin_y+2*Lb],
                       4: [building_origin_x+7*Lb, building_origin_y+3*Lb],
                       5: [building_max_x, building_origin_y+3*Lb],
                       6: [building_max_x, building_origin_y]},
                '1F1': {1: [building_origin_x, building_origin_y],
                        2: [building_origin_x, building_origin_y+0.5*Lb],
                        3: [building_origin_x+2*Lb, building_origin_y+1*Lb],
                        4: [building_origin_x+2*Lb, building_origin_y]},
                '1F2': {1: [building_origin_x+2*Lb, building_origin_y],
                        2: [building_origin_x+2*Lb, building_origin_y+2*Lb],
                        3: [building_origin_x+5*Lb, building_origin_y+2*Lb],
                        4: [building_origin_x+5*Lb, building_origin_y]},
                '1G1': {1: [building_origin_x, building_origin_y+0.5*Lb],
                        2: [building_origin_x, building_origin_y+3*Lb],
                        3: [building_origin_x+2*Lb, building_origin_y+3*Lb],
                        4: [building_origin_x+2*Lb, building_origin_y+1*Lb]},
                '1G2': {1: [building_origin_x, building_origin_y+3*Lb],
                        2: [building_origin_x, building_origin_y+6*Lb],
                        3: [building_origin_x+2*Lb, building_origin_y+6*Lb],
                        4: [building_origin_x+2*Lb, building_origin_y+4*Lb],
                        5: [building_origin_x+7*Lb, building_origin_y+4*Lb],
                        6: [building_origin_x+7*Lb, building_origin_y+2*Lb],
                        7: [building_origin_x+2*Lb, building_origin_y+2*Lb],
                        8: [building_origin_x+2*Lb, building_origin_y+3*Lb]},
                'D': {1: [building_origin_x, building_origin_y+6*Lb],
                      2: [building_origin_x, building_max_y-6*Lb],
                      3: [building_origin_x+4*Lb, building_max_y-6*Lb],
                      4: [building_origin_x+4*Lb, building_max_y-4*Lb],
                      5: [building_origin_x+6*Lb, building_max_y-4*Lb],
                      6: [building_origin_x+6*Lb, building_max_y],
                      7: [building_max_x-6*Lb, building_max_y],
                      8: [building_max_x-6*Lb, building_max_y-4*Lb],
                      9: [building_max_x-4*Lb, building_max_y-4*Lb],
                      10: [building_max_x-4*Lb, building_max_y-6*Lb],
                      11: [building_max_x, building_max_y-6*Lb],
                      12: [building_max_x, building_max_y-4*Lb],
                      13: [building_max_x, building_origin_y+6*Lb],
                      14: [building_max_x-2*Lb, building_origin_y+6*Lb],
                      15: [building_max_x-2*Lb, building_origin_y+4*Lb],
                      16: [building_max_x-7*Lb, building_origin_y+4*Lb],
                      17: [building_max_x-7*Lb, building_origin_y+3*Lb],
                      18: [building_origin_x+7*Lb, building_origin_y+3*Lb],
                      19: [building_origin_x+7*Lb, building_origin_y+4*Lb],
                      20: [building_origin_x+2*Lb, building_origin_y+4*Lb],
                      21: [building_origin_x+2*Lb, building_origin_y+6*Lb]}
                }
    zones = {}
    for key in formulas:
        zones[key] = list(iter(formulas[key].values()))
        zones[key] = build_polygons(zones[key])
    # must use iter() since the
    # values in formulas are inside a nested dict
    # that iter obj is converted to a list using list()
    # for easy passing to build_polygons
    # this lets us have a dict that perserves the key values
    # so that each zone can have a label when graphed
    return zones
