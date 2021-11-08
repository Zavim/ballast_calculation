import csv
import sys
import matplotlib.pyplot as plt
from descartes import PolygonPatch
import config
import panels
import builder


# building_filepath = 'csv/bigBuilding.csv'
alberta_filepath = 'csv/albertaGap.csv'
acme_filepath = 'csv/acmeRoof.csv'
# building_filepath = 'csv/building.csv'


class Panel:
    def __init__(self,  width, length, polygon, row_column=0, panel_class=None, An=0, zone='', GCL=0):
        self.width = width
        self.length = length
        self.polygon = polygon
        self.row_column = row_column
        self.panel_class = panel_class
        self.An = An
        self.zone = zone
        self.GCL = GCL


def parse_csv(filepath):
    with open(filepath, 'r') as readFile:
        fieldnames = ["x", "y", "pressure_for_lifting"]
        csv_file = csv.DictReader(readFile, fieldnames)
        # header = csv_file[0]
        coord_row = []
        coordinates = []
        try:
            for row in csv_file:
                try:
                    coord_row.append(float(row['x']))
                    coord_row.append(float(row['y']))
                    coordinates.append(coord_row)
                    coord_row = []
                except ValueError:
                    if row['x'] == 'width':
                        building_width = float(row['y'])
                    if row['x'] == 'length':
                        building_length = float(row['y'])
                    if row['x'] == 'nw height':
                        building_height = float(row['y'])
                    if row['x'] == 'ne height':
                        if building_height != float(row['y']):
                            sys.exit('building is not flat')
                    if row['x'] == 'sw height':
                        if building_height != float(row['y']):
                            sys.exit('building is not flat')
                    if row['x'] == 'se height':
                        if building_height != float(row['y']):
                            sys.exit('building is not flat')
                    pass
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(
                filepath, csv_file.line_num, e))
    return coordinates, building_width, building_length, building_height


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
    # zone_intersections = {}
    for zone in iter(zones):
        for panel in array:
            intersects = panel.polygon.intersects(zones[zone])
            if intersects:
                intersection = (panel.polygon.intersection(
                    zones[zone].buffer(0)))
                if intersection.area > 0.0:
                    intersections[panel] = intersection.area
                    # zone_intersections[zone] = dict(intersections)
                    panel.zone = zone
    # return zone_intersections


def main():
    coords, building_width, building_length, building_height = parse_csv(
        alberta_filepath)
    building_coordinates = builder.calculate_building_coordinates(
        building_width=building_width, building_length=building_length, building_height=building_height)
    building = panels.build_polygons(building_coordinates)
    # max_x, max_y = building.bounds[2], building.bounds[3]
    zones = builder.calculate_zones(building, Lb=building_height)
    array = panels.build_arrays(csv=True, coordinates=coords,
                                module_width=4, module_length=2, gap_length=0)
    # array = build_arrays(module_width=4, module_length=2, gap_length=1, rows=4,
    #                      columns=4, distance_left=10, distance_bottom=400, max_x=max_x, max_y=max_y)
    panels.calculate_load_sharing(array, Lb=building_height)
    # graph_polygons(
    #     building=building, zones=zones, array=array, max_x=building_width, max_y=building_length, show=True)
    intersections = calculate_intersection(array, zones)
    for panel in array:
        print(panel.zone, panel.An)
    # for zone in intersections:
    #     for panel in intersections[zone]:
    #         print('panel:', panel, 'zone:', zone, 'area:', str(
    #             intersections[zone][panel]) + ' sqft.')
    # north_ray, south_ray, east_ray, west_ray = Polygons.check_neighbors(
    #      array, module_width=4, module_length=2)
    # ---debugging---
    # array, north_ray, south_ray, east_ray, west_ray = Polygons.build_arrays(module_width=4, module_length=2, gap_length=1, rows=4,
    #                                                                         columns=4, distance_left=10, distance_bottom=400, max_x=max_x, max_y=max_y)
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
    #         panel.polygon, facecolor='#000050', alpha=.75))

    # plt.show()


if __name__ == '__main__':
    main()
