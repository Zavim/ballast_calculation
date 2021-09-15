import csv
import sys
from geopandas.plotting import _plot_polygon_collection
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd

from shapely.geometry import Polygon
from descartes import PolygonPatch

zones_filepath = 'csv/zones.csv'
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
    def graph_polygons(building=None, zones=None, panels=None, show=True):
        # p = gpd.GeoSeries(polygon_list)
        # fig, ax = plt.subplots(subplot_kw=dict(aspect='equal'))
        # col = _plot_polygon_collection(ax, p.geometry)
        # col.set_array(np.array([0, 1, 0]))
        # if show:
        #     plt.show()
        fig, ax = plt.subplots(subplot_kw=dict(aspect='equal'))
        ax.set_xlim(0, 20)
        ax.set_ylim(0, 20)
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
    zones_coordinates = Polygons.parse_csv(zones_filepath)
    building = Polygons.build_polygons(building_coordinates)
    zones = Polygons.build_polygons(zones_coordinates)
    graph = Polygons.graph_polygons(building, zones)
    # graph = Polygons.graph_polygons(building)
    # intersection = Polygons.calculate_intersection(series)

    # zones = Polygons.coordinate_parser(zones_filepath)
    # print(building)
    # print(zones)


if __name__ == '__main__':
    main()
