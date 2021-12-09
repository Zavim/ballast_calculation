from flask import Flask
import matplotlib.pyplot as plt

from shapely.geometry import Polygon, LineString
from shapely.strtree import STRtree
from descartes import PolygonPatch

zones_filepath = 'csv/zones.csv'
zone_formulas_filepath = 'csv/zoneFormulas.csv'
building_filepath = 'csv/bigBuilding.csv'

app = Flask(__name__)


class Panel:
    def __init__(self,  width, length, polygon, row_column, panel_class=None):
        self.width = width
        self.length = length
        self.polygon = polygon
        self.row_column = row_column
        self.panel_class = panel_class


def calculate_building_coordinates(default=False):
    if default:
        coordinates = [[0.0, 0.0], [0.0, 500.0],
                       [500.0, 500.0], [500.0, 0.0]]
        Lb = 15
        return coordinates, Lb

    width = input('input width: ')
    length = input('input length: ')
    Lb = float(input('input height: '))
    coordinates = [[0.0, 0.0], [0.0, float(length)], [float(
        width), float(length)], [float(width), 0.0]]
    return coordinates, Lb


def build_polygons(coordinates):
    polygon = Polygon(coordinates)
    return polygon


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


def build_arrays(num_arrays=0, rows=0, columns=0, module_width=0, module_length=0, gap_length=0, distance_left=0, distance_bottom=0, max_x=0, max_y=0):
    margin_left = LineString([[distance_left, max_y], [distance_left, 0]])
    margin_bottom = LineString(
        [[0, distance_bottom], [max_x, distance_bottom]])
    array_origin = margin_left.intersection(margin_bottom)
    panel_list = []
    array = []
    for row in range(rows):
        gap = gap_length if row >= 1 else 0
        for column in range(columns):
            panel_coordinates = [[array_origin.x + (column*module_width), array_origin.y+(row*module_length)+(row*gap)], [array_origin.x + (column*module_width), array_origin.y+module_length + (row*module_length)+(row*gap)],
                                 [array_origin.x + module_width + (column*module_width), array_origin.y+module_length + (row*module_length)+(row*gap)], [array_origin.x + module_width + (column*module_width), array_origin.y+(row*module_length)+(row*gap)]]
            row_column = (str(row+1)+','+str(column+1))
            # this variable represents each panel's row,column accounting for zero-indexing
            panel = Panel(module_width, module_length,
                          Polygon(panel_coordinates), row_column)
            array.append(panel)
    for panel in array:
        panel_list.append(panel.polygon)
    panel_tree = STRtree(panel_list)
    check_neighbors(
        array, panel_tree, module_width, module_length)
    # --debugging--
    # north_ray, south_ray, east_ray, west_ray = Polygons.check_neighbors(
    #     array, panel_tree, module_width, module_length)
    return array


def check_neighbors(array, panel_tree, module_width, module_length):
    # neighbor_dist = .5
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
        print(panel.row_column, panel.panel_class)
        print('--')
    return north_ray, south_ray, east_ray, west_ray


def classify_panels(neighbor_n=False, neighbor_e=False, neighbor_s=False, neighbor_w=False):
    panel_value = bool(neighbor_w)*(2**0)+bool(neighbor_e) * \
        (2**1)+bool(neighbor_s)*(2**2)+bool(neighbor_n)*(2**3)
    panel_class = 'inside' if panel_value == 15 else 'edge'
    if (panel_value == 0 or panel_value == 5 or panel_value == 6 or panel_value == 9 or panel_value == 10):
        panel_class = 'corner'
    return panel_class


def calculate_load_sharing(array):
    lift_graph = {'An': {1: 10, 2: 20, 3: 30, 4: 40, 5: 50, 6: 60, 7: 70, 8: 80, 9: 90, 10: 100, 11: 200, 12: 300, 13: 400, 14: 500, 15: 600, 16: 700, 17: 800, 18: 900, 19: 1000, 20: 2000},
                  'A1': {1: -.72, 2: -.59, 3: -.51, 4: -.46, 5: -.42, 6: -.38, 7: -.35, 8: -.33, 9: -.3, 10: -.29, 11: -.19, 12: -.14, 13: -.12, 14: -.1, 15: -0.09, 16: -0.08, 17: -0.07, 19: -0.06, 20: -0.05, 21: -0.04},
                  'A2': {1: -0.67, 2: -0.54, 3: -0.47, 4: -0.42, 5: -0.38, 6: -0.35, 7: -0.32, 8: -0.29, 9: -0.27, 10: -0.25, 11: -0.16, 12: -0.11, 13: -0.09, 14: -0.08, 15: -0.07, 16: -0.06, 17: -0.05, 18: -0.04, 19: -0.03, 20: -.02},
                  'B': {1: -0.56, 2: -0.46, 3: -0.4, 4: -0.35, 5: -0.33, 6: -0.3, 7: -0.28, 8: -0.26, 9: -0.24, 10: -0.23, 11: -0.15, 12: -0.1, 13: -0.09, 14: -0.07, 15: -0.06, 16: -0.05, 17: -0.04, 18: -0.03, 19: -0.02, 20: -0.01},
                  'C': {1: -0.33, 2: -0.27, 3: -0.24, 4: -0.22, 5: -0.2, 6: -0.19, 7: -0.17, 8: -0.16, 9: -0.15, 10: -0.14, 11: -0.1, 12: -0.09, 13: -0.08, 14: -0.07, 15: -0.06, 16: -0.05, 17: -0.04, 18: -0.03, 19: -0.02, 20: -.01},
                  'E': {1: -0.39, 2: -0.33, 3: -0.3, 4: -0.27, 5: -0.26, 6: -0.25, 7: -0.23, 8: -0.22, 9: -0.21, 10: -0.2, 11: -0.15, 12: -0.13, 13: -0.11, 14: -0.1, 15: -0.09, 16: -0.08, 17: -0.07, 18: -0.06, 19: -0.05, 20: -.04},
                  'F1': {1: -1.06, 2: -0.9, 3: -0.8, 4: -0.73, 5: -0.68, 6: -0.64, 7: -0.6, 8: -0.57, 9: -0.54, 10: -0.51, 11: -0.38, 12: -0.31, 13: -0.26, 14: -0.23, 15: -0.2, 16: -0.18, 17: -0.17, 18: -0.16, 19: -0.14, 20: -0.1},
                  'F2': {1: -0.48, 2: -0.42, 3: -0.37, 4: -0.34, 5: -0.32, 6: -0.3, 7: -0.29, 8: -0.27, 9: -0.26, 10: -0.25, 11: -0.19, 12: -0.16, 13: -0.13, 14: -0.12, 15: -0.11, 16: -0.1, 17: -0.09, 18: -0.08, 19: -0.07, 20: -0.05},
                  'G1': {1: -0.56, 2: -0.48, 3: -0.43, 4: -0.4, 5: -0.37, 6: -0.35, 7: -0.33, 8: -0.31, 9: -0.29, 10: -0.29, 11: -0.21, 12: -0.17, 13: -0.15, 14: -0.13, 15: -0.12, 16: -0.11, 17: -0.1, 18: -0.09, 19: -0.08, 20: -0.06},
                  'G2': {1: -0.3, 2: -0.25, 3: -0.22, 4: -0.2, 5: -0.19, 6: -0.17, 7: -0.16, 8: -0.15, 9: -0.14, 10: -0.13, 11: -0.1, 12: -0.09, 13: -0.08, 14: -0.07, 15: -0.06, 16: -0.05, 17: -0.04, 18: -0.03, 19: -0.02, 20: -0.01}}


def graph_polygons(building=None, zones=None, array=None, max_x=0, max_y=0, show=True):
    colors = {'3A1': '#c00000',
              '1E': '#00b050',
              '3A2': '#ff00ff',
              '3B': '#ffc000',
              '3C': '#0070c0',
              '4E': '#00b050',
              '4F1': '#7030a0',
              '4F2': '#61bed4',
              '4G1': '#b3a2c7',
              '4G2': '#98b954',
              '2A1': '#c00000',
              '2A2': '#ff00ff',
              '2B': '#ffc000',
              '2C': '#0070c0',
              '1F1': '#7030a0',
              '1F2': '#61bed4',
              '1G1': '#b3a2c7',
              '1G2': '#98b954',
              'D': '#ff0000'
              }
    fig, ax = plt.subplots(subplot_kw=dict(aspect='equal'))
    ax.set_xlim(0, max_x)
    ax.set_ylim(0, max_y)
    if show:
        if building:
            ax.add_artist(PolygonPatch(building, alpha=.25))
        if zones:
            for zone in zones:
                ax.add_artist(PolygonPatch(
                    zones[zone], facecolor=colors[zone], alpha=.5))
                ax.text(zones[zone].centroid.x,
                        zones[zone].centroid.y, zone)
                # centroid represents the center of the polygon
        if array:
            for panel in array:
                ax.add_artist(PolygonPatch(
                    panel.polygon, facecolor='#000050', alpha=.75))
        plt.show()
    return ax


def calculate_intersection(array, zones):
    intersections = {}
    zone_intersections = {}
    for zone in iter(zones):
        for panel in array:
            intersects = panel.polygon.intersects(zones[zone])
            if intersects:
                intersection = (panel.polygon.intersection(
                    zones[zone].buffer(0)))
                if intersection.area > 0.0:
                    intersections[panel] = intersection.area
                    zone_intersections[zone] = dict(intersections)
    return zone_intersections


@app.route("/members")
def main():
    building_coordinates, Lb = calculate_building_coordinates(True)
    return {'building': building_coordinates, 'height': Lb}
    # building = Polygons.build_polygons(building_coordinates)
    # max_x, max_y = building.bounds[2], building.bounds[3]
    # zones = Polygons.calculate_zones(building, Lb=Lb)
    # array = Polygons.build_arrays(module_width=4, module_length=2, gap_length=1, rows=4,
    #                               columns=4, distance_left=10, distance_bottom=400, max_x=max_x, max_y=max_y)
    # Polygons.graph_polygons(
    #     building=building, zones=zones, array=array, max_x=max_x, max_y=max_y, show=False)


if __name__ == "__main__":
    app.run(debug=True)
