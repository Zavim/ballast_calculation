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
building_filepath = 'csv/building.csv'
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
    def parse_zones(filepath, building):
        with open(filepath, 'r') as readFile:
            csv_file = csv.DictReader(readFile)
            BX3 = 49
            BY3 = 80
            Lb = 10
            try:
                for row in csv_file:
                    formula = row['Formula']
                    tree = ast.parse(formula)
                    # ast solution wont work TODO: hardcode the formulas into a dict or something
                    # max_x = building[0].exterior.coords[1][0]
                    # max_y = building[0].exterior.coords[1][1]
                formuler = ast.unparse(tree)
                print(ast.literal_eval(formuler))
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(
                    filepath, csv_file.line_num, e))

    @staticmethod
    def graph_polygons(building=None, zones=None, panels=None, show=True):
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
        # col = _plot_polygon_collection(ax, p.geometry)
        # col.set_array(np.array([0, 1, 0]))
        # triangle = polygon_list[0]
        # square = polygon_list[1]
        # print(square)
        for polygon in building:
            ax.add_artist(PolygonPatch(polygon, alpha=.25))
        for polygon in zones:
            ax.add_artist(PolygonPatch(polygon, alpha=.5))
        # for polygon in panels:
        # panel coordinates are calculated from the center of the panel,
        # bottom left of the roof
        #     ax.add_artist(PolygonPatch(polygon, alpha=.5))
        if show:
            plt.show()

    @staticmethod
    def calculate_intersection(series):
        for i in range(len(series)):
            for j in range(1, len(series)):
                if not j == i:
                    intersects = (series[i].intersects(series[j]))
                    if intersects:
                        intersection = (series[i].intersection(series[j]))
                        if intersection.area > 0.0:
                            print(intersection.area)


def main():
    building_coordinates = Polygons.parse_csv(building_filepath)
    # zones_coordinates = Polygons.parse_csv(zones_filepath)
    building = Polygons.build_polygons(building_coordinates)
    # zones = Polygons.build_polygons(zones_coordinates)
    # graph = Polygons.graph_polygons(building, zones)
    # intersection = Polygons.calculate_intersection(series)

    formulas = Polygons.parse_zones(zone_formulas_filepath, building)
    # print(formulas)


if __name__ == '__main__':
    main()
