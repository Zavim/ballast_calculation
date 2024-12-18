from scipy import interpolate
from shapely.geometry import Polygon, LineString
from shapely.strtree import STRtree
import math
import output


class Array:
    def __init__(self, index, panel_list, ns_gap, ew_gap):
        self.index = index
        self.panel_list = panel_list
        self.array_total = len(panel_list)
        self.rows = panel_list[-1].index[0]+1
        self.columns = panel_list[-1].index[1]+1
        self.ns_gap = ns_gap
        self.ew_gap = ew_gap


class Panel:
    def __init__(self,  index, width, length, polygon, panel_class=None, load_share_factor=None, AtribL=0, AtribS=0, AnL=0, AnS=0, zones={}, vortex_zones={}, gcl=0, gcs=0, gamma_e=1, forceL=0, forceS=0):
        self.index = index
        self.width = width
        self.length = length
        self.polygon = polygon
        self.panel_class = panel_class
        self.load_share_factor = load_share_factor
        self.AtribL = AtribL
        self.AtribS = AtribS
        self.AnL = AnL
        self.AnS = AnS
        self.zones = zones
        self.vortex_zones = vortex_zones
        self.gcl = gcl
        self.gcs = gcs
        self.gamma_e = gamma_e
        self.forceL = forceL
        self.forceS = forceS


parameter_dict = {}


def build_arrays(zones=None, vortex_zones=None, building=None, csv_coordinates=None, rows=0, columns=0, module_width=0, module_length=0, gap_length=0, distance_left=0, distance_bottom=0, report=False):
    array = []
    panel_polygon_list = []
    panel_tree = []
    panel_count = []

    W = max(building.length, building.width)
    z = building.height
    Lb = min(z, 0.4 * (W * z) ** 1/2)
    max_x = building.length
    max_y = building.width
    append_parameter_dict('W', W, parameter_dict)
    append_parameter_dict('w', building.width, parameter_dict)
    append_parameter_dict('l', building.length, parameter_dict)
    append_parameter_dict('z', z, parameter_dict)
    append_parameter_dict('Lb', Lb, parameter_dict)

    if csv_coordinates:
        for pair in csv_coordinates:
            panel_origin = dict(x=pair[0], y=pair[1])
            panel_coordinates = [[panel_origin['x'] + (module_width), panel_origin['y']+(module_length)], [panel_origin['x'] + (module_width), panel_origin['y']+module_length + (module_length)],
                                 [panel_origin['x'] + module_width + (module_width), panel_origin['y']+module_length + (module_length)], [panel_origin['x'] + module_width + (module_width), panel_origin['y']+(module_length)]]
            panel = Panel(index=None, width=module_width,
                          length=module_length, polygon=Polygon(panel_coordinates))
            array.append(panel)
    else:
        margin_left = LineString([[distance_left, max_y], [distance_left, 0]])
        margin_bottom = LineString(
            [[0, distance_bottom], [max_x, distance_bottom]])
        array_origin = margin_left.intersection(margin_bottom)
        for row in range(rows):
            gap = gap_length if row >= 1 else 0
            for column in range(columns):
                panel_count = [row, column]
                panel_coordinates = [[array_origin.x + (column*module_width), array_origin.y+(row*module_length)+(row*gap)], [array_origin.x + (column*module_width), array_origin.y+module_length + (row*module_length)+(row*gap)],
                                     [array_origin.x + module_width + (column*module_width), array_origin.y+module_length + (row*module_length)+(row*gap)], [array_origin.x + module_width + (column*module_width), array_origin.y+(row*module_length)+(row*gap)]]
                panel = Panel(index=panel_count, width=module_width,
                              length=module_length, polygon=Polygon(panel_coordinates))
                array.append(panel)

    for panel in array:
        panel_polygon_list.append(panel.polygon)
    panel_tree = STRtree(panel_polygon_list)
    check_neighbors(
        array, panel_tree, module_width, module_length)
    calculate_panel_zones(array, zones)
    calculate_vortex_zones(array, vortex_zones)
    calculate_edge_factors(array)
    calculate_lift_and_friction(array, Lb)
    calculate_forces(array=array, building=building,
                     Lb=Lb, parameter_dict=parameter_dict)
    # --debugging--
    # north_ray, south_ray, east_ray, west_ray = Polygons.check_neighbors(
    #     array, panel_tree, module_width, module_length)
    return array


def append_parameter_dict(key=None, value=None, parameter_dict=None):
    parameter_dict[key] = value


def generateReport(report=False, arrays=None, parameter_dict=None):
    if report:
        report_name, file, writer = output.write_parameters(
            parameter_dict, arrays[0])
        for array in arrays:
            output.write_panels(report_name=report_name, file=file, writer=writer, array=array,
                                parameter_dict=parameter_dict)


def check_neighbors(array, panel_tree, module_width, module_length):
    # neighbor_dist = 4  # alberta
    neighbor_dist = .5 + 11/12
    # 6 inches == half a ft, 11/12 is the 11in gap length on Acme building
    for panel in array:
        north_ray = LineString([[panel.polygon.centroid.x, panel.polygon.centroid.y+(.5*module_length)+.05], [
                                panel.polygon.centroid.x, panel.polygon.centroid.y+(.5*module_length)+neighbor_dist]])

        east_ray = LineString([[panel.polygon.centroid.x+(.5*module_width)+.05, panel.polygon.centroid.y], [
            panel.polygon.centroid.x+(.5*module_width)+neighbor_dist, panel.polygon.centroid.y]])

        south_ray = LineString([[panel.polygon.centroid.x, panel.polygon.centroid.y-(.5*module_length)-.05], [
                                panel.polygon.centroid.x, panel.polygon.centroid.y-(.5*module_length)-neighbor_dist]])

        west_ray = LineString([[panel.polygon.centroid.x-(.5*module_width)-.05, panel.polygon.centroid.y], [
            panel.polygon.centroid.x-(.5*module_width)-neighbor_dist, panel.polygon.centroid.y]])

        neighbor_n = bool([panel.wkt for panel in panel_tree.query(
            north_ray) if panel.intersects(north_ray)])

        neighbor_e = bool([panel.wkt for panel in panel_tree.query(
            east_ray) if panel.intersects(east_ray)])

        neighbor_s = bool([panel.wkt for panel in panel_tree.query(
            south_ray) if panel.intersects(south_ray)])

        neighbor_w = bool([panel.wkt for panel in panel_tree.query(
            west_ray) if panel.intersects(west_ray)])

        # print(panel, 'N:', neighbor_n)
        # print(panel, 'E:', neighbor_e)
        # print(panel, 'S:', neighbor_s)
        # print(panel, 'W:', neighbor_w)
        panel.panel_class = classify_panels(
            neighbor_n, neighbor_e, neighbor_s, neighbor_w)
        # print(panel_value)
        # print(panel.row_column, panel.panel_class)
        # print('--')
    # return north_ray, south_ray, east_ray, west_ray


def calculate_panel_zones(array, zones):
    panel_zones = {}
    for panel in array:
        for zone in iter(zones):
            intersects = panel.polygon.intersects(zones[zone])
            if intersects:
                intersection = (panel.polygon.intersection(
                    zones[zone].buffer(0)))
                if intersection.area > 0.0:
                    if zone not in panel_zones:
                        panel_zones[zone] = round(intersection.area, 5)
                        panel.zones = panel_zones
        panel_zones = {}
    # intersections[panel.index] = intersection.area
    # zone_intersections[zone] = dict(intersections)
    # print(intersections)
    # return zone_intersections


def calculate_vortex_zones(array, vortex_zones):
    panel_vortex_zones = {}
    for panel in array:
        for vortex_zone in iter(vortex_zones):
            intersects = panel.polygon.intersects(vortex_zones[vortex_zone])
            if intersects:
                intersection = (panel.polygon.intersection(
                    vortex_zones[vortex_zone].buffer(0)))
                if intersection.area > 0.0 and vortex_zone not in panel_vortex_zones:
                    panel_vortex_zones[vortex_zone] = round(
                        intersection.area, 5)
                    panel.vortex_zones = panel_vortex_zones
        panel_vortex_zones = {}


def classify_panels(neighbor_n=False, neighbor_e=False, neighbor_s=False, neighbor_w=False):
    panel_value = bool(neighbor_w)*(2**0)+bool(neighbor_e) * \
        (2**1)+bool(neighbor_s)*(2**2)+bool(neighbor_n)*(2**3)
    panel_class_dict = {
        0: 'single',
        5: 'ne corner',
        6: 'nw corner',
        7: 'north edge',
        9: 'se corner',
        10: 'sw corner',
        11: 'south edge',
        13: 'east edge',
        14: 'west edge',
        15: 'interior'
    }
    panel_class = panel_class_dict[panel_value]
    return panel_class


def extrapolate(x_dict, y_dict, lookup_value):
    x = []
    y = []
    for key in x_dict:
        x.append(x_dict[key])
    for key in y_dict:
        y.append(y_dict[key])
    extrapolator = interpolate.interp1d(x, y, fill_value="extrapolate")
    return extrapolator(lookup_value)


def calculate_lift_and_friction(array, Lb):
    # Aref == panel area
    # Aref = 21  -- ANISA
    # tributary area == Aref * load share factor
    lift_graph = {'An': {1: 10, 2: 20, 3: 30, 4: 40, 5: 50, 6: 60, 7: 70, 8: 80, 9: 90, 10: 100, 11: 200, 12: 300, 13: 400, 14: 500, 15: 600, 16: 700, 17: 800, 18: 900, 19: 1000, 20: 2000},
                  'A1': {1: -0.72, 2: -0.59, 3: -0.51, 4: -0.46, 5: -0.42, 6: -0.38, 7: -0.35, 8: -0.33, 9: -0.3, 10: -0.29, 11: -0.19, 12: -0.14, 13: -0.12, 14: -0.1, 15: -0.09, 16: -0.08, 17: -0.07, 18: -0.06, 19: -0.05, 20: -0.04},
                  'A2': {1: -0.67, 2: -0.54, 3: -0.47, 4: -0.42, 5: -0.38, 6: -0.35, 7: -0.32, 8: -0.29, 9: -0.27, 10: -0.25, 11: -0.16, 12: -0.11, 13: -0.09, 14: -0.08, 15: -0.07, 16: -0.06, 17: -0.05, 18: -0.04, 19: -0.03, 20: -.02},
                  'B': {1: -0.56, 2: -0.46, 3: -0.4, 4: -0.35, 5: -0.33, 6: -0.3, 7: -0.28, 8: -0.26, 9: -0.24, 10: -0.23, 11: -0.15, 12: -0.1, 13: -0.09, 14: -0.07, 15: -0.06, 16: -0.05, 17: -0.04, 18: -0.03, 19: -0.02, 20: -0.01},
                  'C': {1: -0.33, 2: -0.27, 3: -0.24, 4: -0.22, 5: -0.2, 6: -0.19, 7: -0.17, 8: -0.16, 9: -0.15, 10: -0.14, 11: -0.1, 12: -0.09, 13: -0.08, 14: -0.07, 15: -0.06, 16: -0.05, 17: -0.04, 18: -0.03, 19: -0.02, 20: -.01},
                  'E': {1: -0.39, 2: -0.33, 3: -0.3, 4: -0.27, 5: -0.26, 6: -0.25, 7: -0.23, 8: -0.22, 9: -0.21, 10: -0.2, 11: -0.15, 12: -0.13, 13: -0.11, 14: -0.1, 15: -0.09, 16: -0.08, 17: -0.07, 18: -0.06, 19: -0.05, 20: -.04},
                  'F1': {1: -1.06, 2: -0.9, 3: -0.8, 4: -0.73, 5: -0.68, 6: -0.64, 7: -0.6, 8: -0.57, 9: -0.54, 10: -0.51, 11: -0.38, 12: -0.31, 13: -0.26, 14: -0.23, 15: -0.2, 16: -0.18, 17: -0.17, 18: -0.16, 19: -0.14, 20: -0.1},
                  'F2': {1: -0.48, 2: -0.42, 3: -0.37, 4: -0.34, 5: -0.32, 6: -0.3, 7: -0.29, 8: -0.27, 9: -0.26, 10: -0.25, 11: -0.19, 12: -0.16, 13: -0.13, 14: -0.12, 15: -0.11, 16: -0.1, 17: -0.09, 18: -0.08, 19: -0.07, 20: -0.05},
                  'G1': {1: -0.56, 2: -0.48, 3: -0.43, 4: -0.4, 5: -0.37, 6: -0.35, 7: -0.33, 8: -0.31, 9: -0.29, 10: -0.29, 11: -0.21, 12: -0.17, 13: -0.15, 14: -0.13, 15: -0.12, 16: -0.11, 17: -0.1, 18: -0.09, 19: -0.08, 20: -0.06},
                  'G2': {1: -0.3, 2: -0.25, 3: -0.22, 4: -0.2, 5: -0.19, 6: -0.17, 7: -0.16, 8: -0.15, 9: -0.14, 10: -0.13, 11: -0.1, 12: -0.09, 13: -0.08, 14: -0.07, 15: -0.06, 16: -0.05, 17: -0.04, 18: -0.03, 19: -0.02, 20: -0.01}}

    mu8_graph = {'An': {1: 10, 2: 20, 3: 30, 4: 40, 5: 50, 6: 60, 7: 70, 8: 80, 9: 90, 10: 100,
                        11: 200, 12: 300, 13: 400, 14: 500, 15: 600, 16: 700, 17: 800, 18: 900, 19: 1000, 20: 2000},
                 'A1': {1: -0.91, 2: -0.75, 3: -0.66, 4: -0.6, 5: -0.55, 6: -0.51, 7: -0.47, 8: -0.45, 9: -0.43, 10: -0.4, 11: -0.26, 12: -0.2, 13: -0.18, 14: -0.14, 15: -0.12, 16: -0.11, 17: -0.1, 18: -0.09, 19: -0.07, 20: -0.05},
                 'A2': {1: -0.85, 2: -0.65, 3: -0.57, 4: -0.52, 5: -0.46, 6: -0.43, 7: -0.4, 8: -0.35, 9: -0.33, 10: -0.3, 11: -0.18, 12: -0.15, 13: -0.11, 14: -0.1, 15: -0.08, 16: -0.08, 17: -0.07, 18: -0.06, 19: -0.05, 20: -0.04},
                 'B': {1: -0.75, 2: -0.62, 3: -0.54, 4: -0.48, 5: -0.44, 6: -0.4, 7: -0.38, 8: -0.35, 9: -0.33, 10: 0.3, 11: -0.2, 12: -0.15, 13: -0.14, 14: -0.13, 15: -0.1, 16: -0.09, 17: -0.08, 18: -0.07, 19: -0.06, 20: -0.05},
                 'C': {1: -0.37, 2: -0.31, 3: -0.28, 4: -0.26, 5: -0.24, 6: -0.23, 7: -0.21, 8: -0.2, 9: -0.19, 10: -0.18, 11: -0.13, 12: -0.11, 13: -0.09, 14: -0.08, 15: -0.07, 16: -0.06, 17: -0.05, 18: -0.04, 19: -0.03, 20: -0.02},
                 'E': {1: -0.45, 2: -0.39, 3: -0.36, 4: -0.33, 5: -0.31, 6: -0.30, 7: -0.29, 8: -0.28, 9: -0.26, 10: -0.25, 11: -0.20, 12: -0.17, 13: -0.16, 14: -0.15, 15: -0.14, 16: -0.13, 17: -0.13, 18: -0.11, 19: -0.10, 20: -0.09},
                 'F1': {1: -1.41, 2: -1.2, 3: -1.07, 4: -0.97, 5: -0.9, 6: -0.85, 7: -0.8, 8: -0.75, 9: -0.71, 10: -0.68, 11: -0.5, 12: -0.41, 13: -0.35, 14: -0.31, 15: -0.28, 16: -0.25, 17: -0.23, 18: -0.21, 19: -0.2, 20: -0.17},
                 'G1': {1: -0.65, 2: -0.56, 3: -0.52, 4: -0.48, 5: -0.46, 6: -0.44, 7: -0.42, 8: -0.4, 9: -0.39, 10: -0.38, 11: -0.3, 12: -0.25, 13: -0.22, 14: -0.19, 15: -0.17, 16: -0.16, 17: -0.15, 18: -0.14, 19: -0.13, 20: -0.09},
                 'G2': {1: -0.33, 2: -0.28, 3: -0.25, 4: -0.23, 5: -0.21, 6: -0.2, 7: -0.19, 8: -0.18, 9: -0.17, 10: -0.16, 11: -0.12, 12: -0.1, 13: -0.09, 14: -0.08, 15: -0.07, 16: -0.06, 17: -0.05, 18: -0.04, 19: -0.03, 20: -0.02}}

    mu5_graph = {'An': {1: 10, 2: 20, 3: 30, 4: 40, 5: 50, 6: 60, 7: 70, 8: 80, 9: 90, 10: 100,
                        11: 200, 12: 300, 13: 400, 14: 500, 15: 600, 16: 700, 17: 800, 18: 900, 19: 1000, 20: 2000},
                 'A1': {1: -1.1, 2: -0.93, 3: -0.82, 4: -0.74, 5: -0.68, 6: -0.63, 7: -0.59, 8: -0.56, 9: -0.53, 10: -0.49, 11: -0.34, 12: -0.26, 13: -0.23, 14: -0.2, 15: -0.17, 16: -0.15, 17: -0.14, 18: -0.13, 19: -0.12, 20: -0.08},
                 'A2': {1: -0.93, 2: -0.76, 3: -0.66, 4: -0.59, 5: -0.53, 6: -0.49, 7: -0.45, 8: -0.41, 9: -0.39, 10: -0.36, 11: -0.23, 12: -0.17, 13: -0.14, 14: -0.12, 15: -0.11, 16: -0.1, 17: -0.09, 18: -0.08, 19: -0.07, 20: -0.06},
                 'B': {1: -0.86, 2: -0.72, 3: -0.63, 4: -0.58, 5: -0.53, 6: -0.5, 7: -0.46, 8: -0.44, 9: -0.42, 10: -0.39, 11: -0.27, 12: -0.21, 13: -0.18, 14: -0.15, 15: -0.13, 16: -0.12, 17: -0.11, 18: -0.1, 19: -0.09, 20: -0.06},
                 'C': {1: -0.43, 2: -0.37, 3: -0.33, 4: -0.3, 5: -0.28, 6: -0.26, 7: -0.25, 8: -0.24, 9: -0.23, 10: -0.22, 11: -0.16, 12: -0.13, 13: -0.11, 14: -0.1, 15: -0.09, 16: -0.08, 17: -0.07, 18: -0.06, 19: -0.05, 20: -0.06},
                 'E': {1: -0.51, 2: -0.45, 3: -0.42, 4: -0.39, 5: -0.38, 6: -0.36, 7: -0.34, 8: -0.33, 9: -0.32, 10: -0.31, 11: -0.25, 12: -0.22, 13: -0.2, 14: -0.19, 15: -0.17, 16: -0.16, 17: -0.15, 18: -0.14, 19: -0.13, 20: -0.1},
                 'F1': {1: -1.65, 2: -1.4, 3: -1.25, 4: -1.15, 5: -1.06, 6: -1.0, 7: -0.95, 8: -0.9, 9: -0.85, 10: -0.81, 11: -0.6, 12: -0.49, 13: -0.43, 14: -0.38, 15: -0.34, 16: -0.3, 17: -0.28, 18: -0.26, 19: -0.24, 20: -0.14},
                 'F2': {1: -0.62, 2: -0.54, 3: -0.5, 4: -0.47, 5: -0.44, 6: -0.42, 7: -0.4, 8: -0.39, 9: -0.38, 10: -0.37, 11: -0.29, 12: -0.25, 13: -0.22, 14: -0.2, 15: -0.18, 16: -0.17, 17: -0.15, 18: -0.14, 19: -0.13, 20: -0.09},
                 'G1': {1: -0.73, 2: -0.65, 3: -0.6, 4: -0.56, 5: -0.54, 6: -0.51, 7: -0.49, 8: -0.48, 9: -0.46, 10: -0.45, 11: -0.37, 12: -0.32, 13: -0.28, 14: -0.25, 15: -0.23, 16: -0.21, 17: -0.19, 18: -0.18, 19: -0.16, 20: -0.1},
                 'G2': {1: -0.35, 2: -0.3, 3: -0.27, 4: -0.25, 5: -0.23, 6: -0.22, 7: -0.21, 8: -0.2, 9: -0.19, 10: -0.18, 11: -0.14, 12: -0.11, 13: -0.1, 14: -0.09, 15: -0.08, 16: -0.07, 17: -0.06, 18: -0.05, 19: -0.04, 20: -0.03}}

    d_graph = {'modules': {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 20, 12: 30, 13: 40, 14: 50, 15: 60, 16: 70, 17: 80, 18: 90, 19: 100},
               'lift': {1: -0.130, 2: -0.105, 3: -0.091, 4: -0.080, 5: -0.073, 6: -0.068, 7: -0.063, 8: -0.060, 9: -0.056, 10: -0.053, 11: -0.039, 12: -0.033, 13: -0.030, 14: -0.028, 15: -0.027, 16: -0.027, 17: -0.026, 18: -0.025, 19: -0.025},
               'mu8': {1: -0.180, 2: -0.145, 3: -0.125, 4: -0.110, 5: -0.102, 6: -0.095, 7: -0.089, 8: -0.084, 9: -0.080, 10: -0.077, 11: -0.060, 12: -0.052, 13: -0.047, 14: -0.044, 15: -0.041, 16: -0.041, 17: -0.041, 18: -0.041, 19: -0.040},
               'mu5': {1: -0.200, 2: -0.166, 3: -0.145, 4: -0.130, 5: -0.121, 6: -0.113, 7: -0.106, 8: -0.101, 9: -0.096, 10: -0.094, 11: -0.078, 12: -0.070, 13: -0.068, 14: -0.065, 15: -0.063, 16: -0.062, 17: -0.062, 18: -0.060, 19: -0.060}}

    qz = 19.9  # ANISA
    for panel in array:
        panel.AnL = (panel.AtribL/Lb**2)*1000
        panel.AnS = (panel.AtribS/Lb**2)*1000

        for zone in panel.zones:
            if zone == 'D':
                panel.gcl = extrapolate(
                    d_graph['modules'], d_graph['lift'], panel.AnL)
                panel.gcl = panel.gcl.tolist()
                # to list is needed because panel.gcl is a numpy array due to the extrapolate function
            else:
                panel.gcl = extrapolate(
                    lift_graph['An'], lift_graph[zone[1:]], panel.AnL)
                panel.gcl = panel.gcl.tolist()

            if zone == 'D':
                panel.gcs = extrapolate(
                    d_graph['modules'], d_graph['mu5'], panel.AnS)
            else:
                panel.gcs = extrapolate(
                    mu5_graph['An'], mu5_graph[zone[1:]], panel.AnS)
            panel.gcs = panel.gcs.tolist()


def calculate_edge_factors(array):
    lift_graph = {'A1': {'north edge': 1.0, 'south edge': 1.0, 'east/west edge': 1.0},
                  'B': {'north edge': 1.0, 'south edge': 1.0, 'east/west edge': 1.0},
                  'A2': {'north edge': 1.0, 'south edge': 1.0, 'east/west edge': 1.3},
                  'C': {'north edge': 1.0, 'south edge': 1.0, 'east/west edge': 1.9},
                  'D': {'north edge': 1.0, 'south edge': 1.5, 'east/west edge': 1.6},
                  'E': {'north edge': 1.0, 'south edge': 1.0, 'east/west edge': 1.1},
                  'F1': {'north edge': 1.0, 'south edge': 1.0, 'east/west edge': 1.9},
                  'F2': {'north edge': 1.0, 'south edge': 1.0, 'east/west edge': 1.9},
                  'G1': {'north edge': 1.0, 'south edge': 1.5, 'east/west edge': 1.3},
                  'G2': {'north edge': 1.0, 'south edge': 1.9, 'east/west edge': 1.3}}

    sliding_graph = {'A1': {'north edge': 1.2, 'south edge': 1.0, 'east/west edge': 1.0},
                     'B': {'north edge': 1.2, 'south edge': 1.0, 'east/west edge': 1.0},
                     'A2': {'north edge': 1.0, 'south edge': 1.0, 'east/west edge': 1.2},
                     'C': {'north edge': 1.5, 'south edge': 1.0, 'east/west edge': 1.9},
                     'D': {'north edge': 1.0, 'south edge': 1.0, 'east/west edge': 1.4},
                     'E': {'north edge': 1.0, 'south edge': 1.0, 'east/west edge': 1.1},
                     'F1': {'north edge': 1.0, 'south edge': 1.0, 'east/west edge': 1.7},
                     'F2': {'north edge': 1.0, 'south edge': 1.0, 'east/west edge': 1.7},
                     'G1': {'north edge': 1.0, 'south edge': 1.3, 'east/west edge': 1.2},
                     'G2': {'north edge': 1.0, 'south edge': 2.0, 'east/west edge': 1.3}}

    load_share_factors = {'corner': 3, 'edge': 3, 'interior': 6}

    Aref = array[0].width*array[0].length
    array_total = (array[-1].index[0]+1) * (array[-1].index[1]+1)

    for panel in array:
        if panel.panel_class == 'interior':
            panel.load_share_factor = load_share_factors['interior']
            panel.AtribL = Aref*load_share_factors['interior']
            panel.AtribS = Aref*array_total
            continue

        if panel.panel_class == 'ne corner' or panel.panel_class == 'nw corner':
            panel.load_share_factor = load_share_factors['corner']
            panel.AtribL = Aref*load_share_factors['corner']
            panel.AtribS = Aref*array_total

            for zone in panel.zones:
                if zone == 'D':
                    temp_gamma_e = max(
                        lift_graph[zone]['north edge'], lift_graph[zone]['east/west edge'])
                # if len(zone) <= 1:
                #     temp_gamma_e = max(
                #         lift_graph[zone]['south edge'], lift_graph[zone]['east/west edge'])
                    # since we must slice the first char of the zone string eg. 3B -> B,
                    # we have to account for zones that are one character long eg. 'D'
                else:
                    temp_gamma_e = max(
                        lift_graph[zone[1:]]['north edge'], lift_graph[zone[1:]]['east/west edge'])
                if (temp_gamma_e > panel.gamma_e):
                    panel.gamma_e = temp_gamma_e
            continue

        if panel.panel_class == 'se corner' or panel.panel_class == 'sw corner':
            panel.load_share_factor = load_share_factors['corner']
            panel.AtribL = Aref*load_share_factors['corner']
            panel.AtribS = Aref*array_total

            for zone in panel.zones:
                if zone == 'D':
                    temp_gamma_e = max(
                        lift_graph[zone]['south edge'], lift_graph[zone]['east/west edge'])
                else:
                    temp_gamma_e = max(
                        lift_graph[zone[1:]]['south edge'], lift_graph[zone[1:]]['east/west edge'])
                if (temp_gamma_e > panel.gamma_e):
                    panel.gamma_e = temp_gamma_e
            continue

        else:
            panel.load_share_factor = load_share_factors['edge']
            panel.AtribL = Aref*load_share_factors['edge']
            panel.AtribS = Aref*array_total

            vortex_picker(panel, lift_graph)
        # else:
        #     if panel.panel_class == 'east edge' or panel.panel_class == 'west edge':
        #         for zone in panel.zones:
        #             if zone == 'D':
        #                 temp_gamma_e = lift_graph['D']['east/west edge']
        #             if zone == 'E':
        #                 temp_gamma_e = lift_graph['E']['east/west edge']
        #             # if zone[1:] == 'A1':

        #             if (temp_gamma_e > panel.gamma_e):
        #                 panel.gamma_e = temp_gamma_e
        #                 temp_gamma_e = 0

        #     if panel.panel_class == 'south edge':
        #         for zone in panel.zones:
        #             if zone == 'D':
        #                 temp_gamma_e = lift_graph['D']['south edge']
        #             if zone == 'E':
        #                 temp_gamma_e = lift_graph['E']['south edge']

        #             if (temp_gamma_e > panel.gamma_e):
        #                 panel.gamma_e = temp_gamma_e
        #                 temp_gamma_e = 0

        #     if panel.panel_class == 'north edge':
        #         for zone in panel.zones:
        #             if zone == 'D':
        #                 temp_gamma_e = lift_graph['D']['north edge']
        #             if zone == 'E':
        #                 temp_gamma_e = lift_graph['E']['north edge']

        #             if (temp_gamma_e > panel.gamma_e):
        #                 panel.gamma_e = temp_gamma_e
        #                 temp_gamma_e = 0


def vortex_picker(panel, lift_graph):
    for zone in panel.zones:
        if zone == 'D' or zone == 'E':
            if panel.panel_class == 'east edge' or panel.panel_class == 'west edge':
                temp_gamma_e = lift_graph[zone]['east/west edge']
            else:
                temp_gamma_e = lift_graph[zone][panel.panel_class]

            if temp_gamma_e > panel.gamma_e:
                panel.gamma_e = temp_gamma_e

        else:
            for vortex_zone in panel.vortex_zones:
                if vortex_zone == 'VNE-E':
                    temp_gamma_e = lift_graph[zone[1:]]['east/west edge']
                if vortex_zone == 'VNE-N':
                    temp_gamma_e = lift_graph[zone[1:]]['north edge']
                if vortex_zone == 'VSE-E':
                    temp_gamma_e = lift_graph[zone[1:]]['east/west edge']
                if vortex_zone == 'VSE-S':
                    temp_gamma_e = lift_graph[zone[1:]]['south edge']
                if vortex_zone == 'VNW-W':
                    temp_gamma_e = lift_graph[zone[1:]]['east/west edge']
                if vortex_zone == 'VNW-N':
                    temp_gamma_e = lift_graph[zone[1:]]['north edge']
                if vortex_zone == 'VSW-W':
                    temp_gamma_e = lift_graph[zone[1:]]['east/west edge']
                if vortex_zone == 'VSW-S':
                    temp_gamma_e = lift_graph[zone[1:]]['south edge']

                if temp_gamma_e > panel.gamma_e:
                    panel.gamma_e = temp_gamma_e


def calculate_forces(array=None, building=None, Lb=0, Aref=0, parameter_dict=None, elevation=2500, wind_speed=100):
    Aref = array[0].length * array[0].width
    z = building.height
    Zg = 900
    alpha = 10
    Kzt = 1
    Kd = .85
    Ke = math.e ** (-.0000362 * elevation)
    v = wind_speed
    # w = building_width  # maybe or MAYBE 528
    # 435,466 is bottom left of A1 array
    h2 = .8
    Ph = 4
    if (z < Zg and z > 15):
        Kz = 2.01 * (z/Zg) ** (2/alpha)
    else:
        print('building height does not fit parameters')

    # Lb = min(z, 0.4 * (w * z) ** 1/2)
    qz = .00256 * Kz * Kzt * Kd * Ke * v ** 2
    if (Ph / Lb >= .2):
        gammaP = 1.12
    else:
        gammaP = .88+(1.2 * (Ph / Lb))

    for panel in array:
        panel.forceL = qz*panel.gcl*panel.gamma_e*gammaP*Aref
        panel.forceS = qz*panel.gcs*panel.gamma_e*gammaP*Aref

    append_parameter_dict('qz', qz, parameter_dict)
    append_parameter_dict('Kz', Kz, parameter_dict)
    append_parameter_dict('building_height', z, parameter_dict)
    append_parameter_dict('Zg', Zg, parameter_dict)
    append_parameter_dict('alpha', alpha, parameter_dict)
    append_parameter_dict('Kzt', Kzt, parameter_dict)
    append_parameter_dict('Kd', Kd, parameter_dict)
    append_parameter_dict('Ke', Ke, parameter_dict)
    append_parameter_dict('elevation', elevation, parameter_dict)
    append_parameter_dict('v', v, parameter_dict)
    append_parameter_dict('gammaP', gammaP, parameter_dict)
    append_parameter_dict('Ph', Ph, parameter_dict)
    append_parameter_dict('h2', h2, parameter_dict)
    append_parameter_dict('LSFc', 3, parameter_dict)
    append_parameter_dict('LSFe', 3, parameter_dict)
    append_parameter_dict('LSFi', 6, parameter_dict)
