import csv
import sys
import ast
from geopandas.plotting import _plot_polygon_collection
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd

from shapely.geometry import Polygon
from descartes import PolygonPatch

zones_filepath = 'csv/zones.csv'
zone_formulas_filepath = 'csv/zoneFormulas.csv'
building_filepath = 'csv/bigBuilding.csv'
array_filepath = 'csv/array.csv'
# building_filepath = 'csv/building.csv'
# coordinates_filepath = 'csv/coordinates.csv'
# coordinates_filepath = 'csv/intersection.csv'


class Polygons():
    @staticmethod
    def parse_csv(filepath):
        with open(filepath, 'r') as readFile:
            csv_file = csv.DictReader(readFile)
            coord_pair = []
            coord_row = []
            coordinates = []
            try:
                for row in csv_file:
                    coord_row.append(float(row['x']))
                    coord_row.append(float(row['y']))
                    coord_pair.append(coord_row)
                    if row['id']:
                        coordinates.append(coord_pair)
                        coord_pair = []
                    coord_row = []
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(
                    filepath, csv_file.line_num, e))
        return coordinates

    @staticmethod
    def build_polygons(coordinates):
        polygon_list = []
        for shape in coordinates:
            polygon = Polygon(shape)
            polygon_list.append(polygon)
        return polygon_list

    @staticmethod
    def calculate_zones(building):
        BX1 = building[0].exterior.coords[3][0]
        BY1 = building[0].exterior.coords[3][1]
        BX2 = building[0].exterior.coords[0][0]
        BY2 = building[0].exterior.coords[0][1]
        BX3 = building[0].exterior.coords[1][0]
        BY3 = building[0].exterior.coords[1][1]
        BX4 = building[0].exterior.coords[2][0]
        BY4 = building[0].exterior.coords[2][1]
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
        coordinates = []
        for key in formulas:
            zones[key] = list(iter(formulas[key].values()))
            coordinates.append(zones[key])
            zones[key] = Polygons.build_polygons(coordinates)
            coordinates = []
            # must use iter() since the
            # values in formulas are inside a nested dict
            # that iter obj is converted to a list using list()
            # for easy passing to build_polygons
            # this lets us have a dict that perserves the key values
            # so that each zone can have a label when graphed
        # print(zones)
        return zones

    @staticmethod
    def graph_polygons(building=None, zones=None, array=None, show=True):
        # p = gpd.GeoSeries(polygon_list)
        # fig, ax = plt.subplots(subplot_kw=dict(aspect='equal'))
        # col = _plot_polygon_collection(ax, p.geometry)
        # col.set_array(np.array([0, 1, 0]))
        # if show:
        #     plt.show()
        fig, ax = plt.subplots(subplot_kw=dict(aspect='equal'))
        max_x = building[0].exterior.coords[1][0]
        max_y = building[0].exterior.coords[1][1]
        ax.set_xlim(0, max_x)
        ax.set_ylim(0, max_y)

        # if building:
        #     for polygon in building:
        #         ax.add_artist(PolygonPatch(polygon, alpha=.25))
        if zones:
            for zone in zones:
                for polygon in iter(zones[zone]):
                    ax.add_artist(PolygonPatch(
                        polygon, facecolor='green', alpha=.5))
                    ax.text(polygon.centroid.x, polygon.centroid.y, zone)
                    # centroid represents the center of the polygon
        if array:
            for polygon in array:
                ax.add_artist(PolygonPatch(polygon, alpha=.75))
        if show:
            plt.show()

    @staticmethod
    def calculate_intersection(array, zones):
        for panel in iter(array):
            for zone in iter(zones):
                intersects = panel.intersects(zone)
                if intersects:
                    intersection = (panel.intersection(zone))
                    if intersection.area > 0.0:
                        print(intersection.area, panel, zone)
        # for i in range(len(series)):
        #     for j in range(1, len(series)):
        #         if not j == i:
        #             intersects = (series[i].intersects(series[j]))
        #             if intersects:
        #                 intersection = (series[i].intersection(series[j]))
        #                 if intersection.area > 0.0:
        #                     print(intersection.area)
        # intersects = (*array.intersects(*zones))
        # if intersects:
        #     intersection = (array.intersection(zones))
        #     if intersection.area > 0.0:
        #         print(intersection.area)
        # print(*array)
        # print(*zones)


def main():
    building_coordinates = Polygons.parse_csv(building_filepath)
    # array_coordinates = Polygons.parse_csv(array_filepath)
    building = Polygons.build_polygons(building_coordinates)
    # array = Polygons.build_polygons(array_coordinates)
    zones = Polygons.calculate_zones(building)
    # print(zones)
    graph = Polygons.graph_polygons(building, zones, show=True)
    # intersection = Polygons.calculate_intersection(array, zones)
    # print(formulas)


if __name__ == '__main__':
    main()
