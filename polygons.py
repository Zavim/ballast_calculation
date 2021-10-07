# import csv
import matplotlib.pyplot as plt

from shapely.geometry import Polygon, LineString
from shapely.strtree import STRtree
from descartes import PolygonPatch

zones_filepath = 'csv/zones.csv'
zone_formulas_filepath = 'csv/zoneFormulas.csv'
building_filepath = 'csv/bigBuilding.csv'
# building_filepath = 'csv/building.csv'


class Polygons():
    # @staticmethod
    # def parse_csv(filepath):
    #     with open(filepath, 'r') as readFile:
    #         csv_file = csv.DictReader(readFile)
    #         coord_row = []
    #         coordinates = []
    #         try:
    #             for row in csv_file:
    #                 coord_row.append(float(row['x']))
    #                 coord_row.append(float(row['y']))
    #                 coordinates.append(coord_row)
    #                 coord_row = []
    #         except csv.Error as e:
    #             sys.exit('file {}, line {}: {}'.format(
    #                 filepath, csv_file.line_num, e))
    #     return coordinates

    @staticmethod
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

    @staticmethod
    def build_polygons(coordinates):
        polygon = Polygon(coordinates)
        return polygon

    @staticmethod
    def calculate_zones(building, Lb=0):
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
            zones[key] = Polygons.build_polygons(zones[key])
        # must use iter() since the
        # values in formulas are inside a nested dict
        # that iter obj is converted to a list using list()
        # for easy passing to build_polygons
        # this lets us have a dict that perserves the key values
        # so that each zone can have a label when graphed
        return zones

    @staticmethod
    def build_arrays(num_arrays=0, rows=0, columns=0, module_width=0, module_length=0, gap_length=0, distance_left=0, distance_bottom=0, max_x=0, max_y=0):
        margin_left = LineString([[distance_left, max_y], [distance_left, 0]])
        margin_bottom = LineString(
            [[0, distance_bottom], [max_x, distance_bottom]])
        array_origin = margin_left.intersection(margin_bottom)
        panel_list = []
        # neighbor_matrix = [[0 for i in range(rows+2)]for j in range(columns+2)]
        # for arrays in range(num_arrays):
        array = {}
        for row in range(rows):
            gap = gap_length if row >= 1 else 0
            for column in range(columns):
                panel = [[array_origin.x + (column*module_width), array_origin.y+(row*module_length)+(row*gap)], [array_origin.x + (column*module_width), array_origin.y+module_length + (row*module_length)+(row*gap)],
                         [array_origin.x + module_width + (column*module_width), array_origin.y+module_length + (row*module_length)+(row*gap)], [array_origin.x + module_width + (column*module_width), array_origin.y+(row*module_length)+(row*gap)]]
                row_column = (str(row+1)+','+str(column+1))
                # this key represents each panel's row,column accounting for zero-indexing
                array[row_column] = panel
        for panel in array:
            array[panel] = Polygon(array[panel])
            panel_list.append(array[panel])
        panel_tree = STRtree(panel_list)
        north_ray, south_ray, east_ray, west_ray = Polygons.check_neighbors(
            array, panel_tree, module_width, module_length)
        return array, north_ray, south_ray, east_ray, west_ray

    @staticmethod
    def check_neighbors(array, panel_tree, module_width, module_length):
        neighbor_dist = .5
        # 6 inches == half a ft
        for panel in array:
            rays = []
            north_ray = LineString([[array[panel].centroid.x, array[panel].centroid.y+(.5*module_length)+.05], [
                                   array[panel].centroid.x, array[panel].centroid.y+(.5*module_length)+neighbor_dist]])

            east_ray = LineString([[array[panel].centroid.x+(.5*module_width)+.05, array[panel].centroid.y], [
                                  array[panel].centroid.x+(.5*module_width)+neighbor_dist, array[panel].centroid.y]])

            south_ray = LineString([[array[panel].centroid.x, array[panel].centroid.y-(.5*module_length)-.05], [
                                   array[panel].centroid.x, array[panel].centroid.y-(.5*module_length)-neighbor_dist]])

            west_ray = LineString([[array[panel].centroid.x-(.5*module_width)-.05, array[panel].centroid.y], [
                                  array[panel].centroid.x-(.5*module_width)-neighbor_dist, array[panel].centroid.y]])

            print(panel, 'N:', bool([panel.wkt for panel in panel_tree.query(
                north_ray) if panel.intersects(north_ray)]))
            print(panel, 'E:', bool([panel.wkt for panel in panel_tree.query(
                east_ray) if panel.intersects(east_ray)]))
            print(panel, 'S:', bool([panel.wkt for panel in panel_tree.query(
                south_ray) if panel.intersects(south_ray)]))
            print(panel, 'W:', bool([panel.wkt for panel in panel_tree.query(
                west_ray) if panel.intersects(west_ray)]))
            print('--')

        return north_ray, south_ray, east_ray, west_ray

    @staticmethod
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
                        array[panel], facecolor='#000050', alpha=.75))
            plt.show()
        return ax

    @ staticmethod
    def calculate_intersection(array, zones):
        intersections = {}
        zone_intersections = {}
        for zone in iter(zones):
            for panel in array:
                intersects = array[panel].intersects(zones[zone])
                if intersects:
                    intersection = (array[panel].intersection(
                        zones[zone].buffer(0)))
                    if intersection.area > 0.0:
                        intersections[panel] = intersection.area
                        zone_intersections[zone] = dict(intersections)
        return zone_intersections


def main():
    building_coordinates, Lb = Polygons.calculate_building_coordinates(True)
    building = Polygons.build_polygons(building_coordinates)
    max_x, max_y = building.bounds[2], building.bounds[3]
    zones = Polygons.calculate_zones(building, Lb=Lb)
    array = Polygons.build_arrays(module_width=4, module_length=2, gap_length=1, rows=4,
                                  columns=4, distance_left=10, distance_bottom=400, max_x=max_x, max_y=max_y)
    # intersections = Polygons.calculate_intersection(array, zones)
    # for zone in intersections:
    #     for panel in intersections[zone]:
    #         print('panel:', panel, 'zone:', zone, 'area:', str(
    #             intersections[zone][panel]) + ' sqft.')
    # north_ray, south_ray, east_ray, west_ray = Polygons.check_neighbors(
    #      array, module_width=4, module_length=2)
    # ---debugging---
    # array, north_ray, south_ray, east_ray, west_ray = Polygons.build_arrays(module_width=4, module_length=2, gap_length=1, rows=4,
    #                                                                         columns=4, distance_left=10, distance_bottom=400, max_x=max_x, max_y=max_y)
    # ax = Polygons.graph_polygons(
    #     building=building, zones=zones, array=array, max_x=max_x, max_y=max_y, show=False)
    # x, y = north_ray.xy
    # ax.plot(x, y)
    # x, y = east_ray.xy
    # ax.plot(x, y)
    # x, y = south_ray.xy
    # ax.plot(x, y)
    # x, y = west_ray.xy
    # ax.plot(x, y)
    # for panel in array:
    #     ax.add_artist(PolygonPatch(
    #         array[panel], facecolor='#000050', alpha=.75))

    # plt.show()


if __name__ == '__main__':
    main()
