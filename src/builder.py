from shapely.geometry import Polygon


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
    return coordinates


def calculate_vortex_zones(building):
    BX1 = building.bounds[0]
    BY1 = building.bounds[1]
    BX2 = building.bounds[0]
    BY2 = building.bounds[3]
    BX3 = building.bounds[2]
    BY3 = building.bounds[3]
    BX4 = building.bounds[2]
    BY4 = building.bounds[1]
#     vortex_formulas = {'VNE-E': {1: [BX1, BY1],
#                                  2: [BX1, BY2], 3: [BX3, BY2], 4: [(BX3-BY2), BY1]},
#                        'VNE-N': {1: [(BX3-BY2), BY1], 2: [BX3, BY2], 3: [BX3, BY1]},
#                        'VNW-W': {1: [BX1, BY2], 2: [BX3, BY2], 3: [BX3, BY1], 4: [BY2, BX1]},
#                        'VNW-N': {1: [BX1, BY1], 2: [BX1, BY2], 3: [BY2, BX1]},
#                        'VSW-W': {1: [BX1, BY1], 2: [BX1, BY2], 3: [BY2, BY2]},
#                        'VSE-E': {1: [BX1, BY1], 2: [BX1, BY2], 3: [(BX3-BY2), BY2], 4: [BX3, BY1]},
#                        'VSE-S': {1: [(BX3-BY2), BY2], 2: [BX3, BY2], 3: [BX3, BY1]}}

    vortex_formulas = {
        'VNE-E': {1: [BX1, BY1], 2: [BX1, BY2], 3: [BX3, BY2]},
        'VNE-N': {1: [(BX3-BY2), BY1], 2: [BX3, BY2], 3: [BX3, BY1]},
        'VNW-W': {1: [BX1, BY2], 2: [BX3, BY2], 3: [BX3, BY1]},
        'VNW-N': {1: [BX1, BY1], 2: [BX1, BY2], 3: [BY2, BX1]},
        'VSW-W': {1: [BX1, BY1], 2: [BX1, BY2], 3: [BY2, BY2]},
        'VSW-S': {1: [(BX3-BY2), BY1], 2: [BX3, BY2], 3: [BX3, BY1]},
        'VSE-E': {1: [BX1, BY1], 2: [BX1, BY2], 3: [(BX3-BY2), BY2]},
        'VSE-S': {1: [(BX3-BY2), BY2], 2: [BX3, BY2], 3: [BX3, BY1]}
    }
    vortex_zones = {}
    for key in vortex_formulas:
        vortex_zones[key] = list(iter(vortex_formulas[key].values()))
        vortex_zones[key] = build_polygons(vortex_zones[key])
    return vortex_zones


def calculate_zones(building, Lb=0):
    # Lb is building height
    BX1 = building.bounds[0]
    BY1 = building.bounds[1]
    BX2 = building.bounds[0]
    BY2 = building.bounds[3]
    BX3 = building.bounds[2]
    BY3 = building.bounds[3]
    BX4 = building.bounds[2]
    BY4 = building.bounds[1]
#     rename these to direction+zone, eg EA2
    formulas = {'3A1': {1: [BX3, BY3],
                        2: [BX3, BY3-2*Lb],
                        3: [BX3-2*Lb, BY3-2*Lb],
                        4: [BX3-0.5*Lb, BY3]},
                '3A2': {1: [BX3-0.5*Lb, BY3],
                        2: [BX3-2*Lb, BY3-2*Lb],
                        3: [BX3-4*Lb, BY3-2*Lb],
                        4: [BX3-4*Lb, BY3]},
                '3B': {1: [BX3, BY3-2*Lb],
                       2: [BX3, BY3-4*Lb],
                       3: [BX3-2*Lb, BY3-4*Lb],
                       4: [BX3-2*Lb, BY3-2*Lb]},
                '3C': {1: [BX3-6*Lb, BY3],
                       2: [BX3-4*Lb, BY3],
                       3: [BX3-4*Lb, BY3-2*Lb],
                       4: [BX3-2*Lb, BY3-2*Lb],
                       5: [BX3-2*Lb, BY3-4*Lb],
                       6: [BX3, BY3-4*Lb],
                       7: [BX3, BY3-6*Lb],
                       8: [BX3-4*Lb, BY3-6*Lb],
                       9: [BX3-4*Lb, BY3-4*Lb],
                       10: [BX3-6*Lb, BY3-4*Lb]},
                '4E': {1: [BX4-5*Lb, BY4+2*Lb],
                       2: [BX4-5*Lb, BY4],
                       3: [BX1, BY1],
                       4: [BX1, BY1+3*Lb],
                       5: [BX4-7*Lb, BY4+3*Lb],
                       6: [BX4-7*Lb, BY4+2*Lb]},
                '4F1': {1: [BX4, BY4],
                        2: [BX4-2*Lb, BY4],
                        3: [BX4-2*Lb, BY4+Lb],
                        4: [BX4, BY4+0.5*Lb]},
                '4F2': {1: [BX4-2*Lb, BY4+2*Lb],
                        2: [BX4-2*Lb, BY4],
                        3: [BX4-5*Lb, BY4],
                        4: [BX4-5*Lb, BY4+2*Lb]},
                '4G1': {1: [BX4, BY4+3*Lb],
                        2: [BX4, BY4+0.5*Lb],
                        3: [BX4-2*Lb, BY4+Lb],
                        4: [BX4-2*Lb, BY4+3*Lb]},
                '4G2': {1: [BX4-2*Lb, BY4+6*Lb],
                        2: [BX4, BY4+6*Lb],
                        3: [BX4, BY4+3*Lb],
                        4: [BX4-2*Lb, BY4+3*Lb],
                        5: [BX4-2*Lb, BY4+2*Lb],
                        6: [BX4-7*Lb, BY4+2*Lb],
                        7: [BX4-7*Lb, BY4+4*Lb],
                        8: [BX4-2*Lb, BY4+4*Lb]},
                '2A1': {1: [BX2, BY2],
                        2: [BX2+0.5*Lb, BY2],
                        3: [BX2+2*Lb, BY2-2*Lb],
                        4: [BX2, BY2-2*Lb]},
                '2A2': {1: [BX2+0.5*Lb, BY2],
                        2: [BX2+4*Lb, BY2],
                        3: [BX2+4*Lb, BY2-2*Lb],
                        4: [BX2+2*Lb, BY2-2*Lb]},
                '2B': {1: [BX2, BY2-2*Lb],
                       2: [BX2+2*Lb, BY2-2*Lb],
                       3: [BX2+2*Lb, BY2-4*Lb],
                       4: [BX2, BY2-4*Lb]},
                '2C': {1: [BX2+4*Lb, BY2],
                       2: [BX2+6*Lb, BY2],
                       3: [BX2+6*Lb, BY2-4*Lb],
                       4: [BX2+4*Lb, BY2-4*Lb],
                       5: [BX2+4*Lb, BY2-6*Lb],
                       6: [BX2, BY2-6*Lb],
                       7: [BX2, BY2-4*Lb],
                       8: [BX2+2*Lb, BY2-4*Lb],
                       9: [BX2+2*Lb, BY2-2*Lb],
                       10: [BX2+4*Lb, BY2-2*Lb]},
                '1E': {1: [BX1+5*Lb, BY1],
                       2: [BX1+5*Lb, BY1+2*Lb],
                       3: [BX1+7*Lb, BY1+2*Lb],
                       4: [BX1+7*Lb, BY1+3*Lb],
                       5: [BX4, BY4+3*Lb],
                       6: [BX4, BY4]},
                '1F1': {1: [BX1, BY1],
                        2: [BX1, BY1+0.5*Lb],
                        3: [BX1+2*Lb, BY1+1*Lb],
                        4: [BX1+2*Lb, BY1]},
                '1F2': {1: [BX1+2*Lb, BY1],
                        2: [BX1+2*Lb, BY1+2*Lb],
                        3: [BX1+5*Lb, BY1+2*Lb],
                        4: [BX1+5*Lb, BY1]},
                '1G1': {1: [BX1, BY1+0.5*Lb],
                        2: [BX1, BY1+3*Lb],
                        3: [BX1+2*Lb, BY1+3*Lb],
                        4: [BX1+2*Lb, BY1+1*Lb]},
                '1G2': {1: [BX1, BY1+3*Lb],
                        2: [BX1, BY1+6*Lb],
                        3: [BX1+2*Lb, BY1+6*Lb],
                        4: [BX1+2*Lb, BY1+4*Lb],
                        5: [BX1+7*Lb, BY1+4*Lb],
                        6: [BX1+7*Lb, BY1+2*Lb],
                        7: [BX1+2*Lb, BY1+2*Lb],
                        8: [BX1+2*Lb, BY1+3*Lb]},
                'D': {1: [BX1, BY1+6*Lb],
                      2: [BX2, BY2-6*Lb],
                      3: [BX2+4*Lb, BY2-6*Lb],
                      4: [BX2+4*Lb, BY2-4*Lb],
                      5: [BX2+6*Lb, BY2-4*Lb],
                      6: [BX2+6*Lb, BY2],
                      7: [BX3-6*Lb, BY3],
                      8: [BX3-6*Lb, BY3-4*Lb],
                      9: [BX3-4*Lb, BY3-4*Lb],
                      10: [BX3-4*Lb, BY3-6*Lb],
                      11: [BX3, BY3-6*Lb],
                      12: [BX3, BY3-4*Lb],
                      13: [BX4, BY4+6*Lb],
                      14: [BX4-2*Lb, BY4+6*Lb],
                      15: [BX4-2*Lb, BY4+4*Lb],
                      16: [BX4-7*Lb, BY4+4*Lb],
                      17: [BX4-7*Lb, BY4+3*Lb],
                      18: [BX1+7*Lb, BY1+3*Lb],
                      19: [BX1+7*Lb, BY1+4*Lb],
                      20: [BX1+2*Lb, BY1+4*Lb],
                      21: [BX1+2*Lb, BY1+6*Lb]}
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
