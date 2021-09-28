import csv
import sys
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd

from shapely.geometry import Polygon, LineString
from descartes import PolygonPatch

zones_filepath = 'csv/zones.csv'
zone_formulas_filepath = 'csv/zoneFormulas.csv'
building_filepath = 'csv/bigBuilding.csv'
# building_filepath = 'csv/building.csv'


class Polygons():
    @staticmethod
    def parse_csv(filepath):
        with open(filepath, 'r') as readFile:
            csv_file = csv.DictReader(readFile)
            coord_row = []
            coordinates = []
            try:
                for row in csv_file:
                    coord_row.append(float(row['x']))
                    coord_row.append(float(row['y']))
                    coordinates.append(coord_row)
                    coord_row = []
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(
                    filepath, csv_file.line_num, e))
        return coordinates

    @staticmethod
    def build_polygons(coordinates):
        polygon = Polygon(coordinates)
        return polygon

    @staticmethod
    def calculate_zones(building):
        BX1 = building.exterior.coords[3][0]
        BY1 = building.exterior.coords[3][1]
        BX2 = building.exterior.coords[0][0]
        BY2 = building.exterior.coords[0][1]
        BX3 = building.exterior.coords[1][0]
        BY3 = building.exterior.coords[1][1]
        BX4 = building.exterior.coords[2][0]
        BY4 = building.exterior.coords[2][1]
        Lb = 15
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
                    '3C': {1: [BX3-4*Lb, BY3],
                           2: [BX3-4*Lb, BY3-2*Lb],
                           3: [BX3-2*Lb, BY3-2*Lb],
                           4: [BX3-2*Lb, BY3-4*Lb],
                           5: [BX3, BY3-4*Lb],
                           6: [BX3, BY3-6*Lb],
                           7: [BX3-4*Lb, BY3-6*Lb],
                           8: [BX3-4*Lb, BY3-4*Lb],
                           9: [BX3-6*Lb, BY3-4*Lb],
                           10: [BX3-6*Lb, BY3]},
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
                    '4G2': {1: [BX4, BY4+6*Lb],
                            2: [BX4, BY4+3*Lb],
                            3: [BX4-2*Lb, BY4+3*Lb],
                            4: [BX4-2*Lb, BY4+2*Lb],
                            5: [BX4-7*Lb, BY4+2*Lb],
                            6: [BX4-7*Lb, BY4+4*Lb],
                            7: [BX4-2*Lb, BY4+4*Lb],
                            8: [BX4-2*Lb, BY4+6*Lb]},
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
                            8: [BX1+2*Lb, BY1+3*Lb]}}
        zones = {}
        for key in formulas:
            zones[key] = list(iter(formulas[key].values()))
            zones[key] = Polygons.build_polygons(zones[key])
            # must use iter() since the
            # values in formulas are inside a nested dict
            # that iter obj is converted to a list using list()
            # for easy passing to build_polygons
            # this lets us have a dict that perserves the key values
            # so that each zone can have a label when graphed
        return zones

    @staticmethod
    def build_array(module_width, module_length, gap_length, rows, columns, distance_left, distance_bottom, max_x, max_y):
        margin_left = LineString([[distance_left, max_y], [distance_left, 0]])
        margin_bottom = LineString(
            [[0, distance_bottom], [max_x, distance_bottom]])
        array_origin = margin_left.intersection(margin_bottom)
        array = []
        for row in range(rows):
            gap = gap_length if row >= 1 else 0
            for column in range(columns):
                panel = [[array_origin.x + (column*module_width), array_origin.y+(row*module_length)+(row*gap)], [array_origin.x + (column*module_width), array_origin.y+module_length + (row*module_length)+(row*gap)],
                         [array_origin.x + module_width + (column*module_width), array_origin.y+module_length + (row*module_length)+(row*gap)], [array_origin.x + module_width + (column*module_width), array_origin.y+(row*module_length)+(row*gap)]]
                array.append(panel)
        for i in range(len(array)):
            array[i] = Polygon(array[i])
        return array

    @staticmethod
    def graph_polygons(building=None, zones=None, array=False, intersection=False, show=True):
        colors = {'3A1': '',
                  '3A2': '',
                  '3B': '',
                  '3C': '',
                  '4E': '',
                  '4F1': '',
                  '4F2': '',
                  '4G1': '',
                  '4G2': '',
                  '2A1': '',
                  '2A2': '',
                  '2B': '',
                  '2C': '',
                  '1E': '',
                  '1F1': '',
                  '1F2': '',
                  '1G1': '',
                  '1G2': ''
                  }
        fig, ax = plt.subplots(subplot_kw=dict(aspect='equal'))
        max_x = building.exterior.coords[1][0]
        max_y = building.exterior.coords[1][1]
        ax.set_xlim(0, max_x)
        ax.set_ylim(0, max_y)

        if building:
            ax.add_artist(PolygonPatch(building, alpha=.25))
        if zones:
            for zone in zones:
                # make another dict for colors
                ax.add_artist(PolygonPatch(
                    zones[zone], facecolor='green', alpha=.5))
                ax.text(zones[zone].centroid.x, zones[zone].centroid.y, zone)
                # centroid represents the center of the polygon
        if array:
            array = Polygons.build_array(4, 2, 1, 4, 4, 10, 400, max_x, max_y)
            for polygon in array:
                ax.add_artist(PolygonPatch(polygon, alpha=.75))
        if intersection:
            Polygons.calculate_intersection(array, zones)
            # return intersection
        if show:
            plt.show()

    @staticmethod
    def calculate_intersection(array, zones):
        for panel in iter(array):
            for zone in iter(zones):
                intersects = panel.intersects(zones[zone])
                if intersects:
                    intersection = (panel.intersection(zones[zone]))
                    if intersection.area > 0.0:
                        print(zone, intersection.area, 'sqft.')


def main():
    building_coordinates = Polygons.parse_csv(building_filepath)
    building = Polygons.build_polygons(building_coordinates)
    zones = Polygons.calculate_zones(building)
    graph = Polygons.graph_polygons(
        building=building, zones=zones, array=True, intersection=True, show=True)


if __name__ == '__main__':
    main()
