import csv
import sys
import matplotlib.pyplot as plt
from descartes import PolygonPatch
import panels
import builder
from panels import parameter_dict


# big_building_filepath = 'csv/bigBuilding.csv'
# alberta_filepath = 'csv/albertaGap.csv'
# acme_filepath = 'csv/acmeRoof.csv'
input_filepath = 'albertaInput.csv'
# input_filepath = 'anisa.csv'
# building_filepath = 'csv/building.csv'


# def parse_csv(filepath):
#     with open(filepath, 'r') as readFile:
#         fieldnames = ["x", "y", "pressure_for_lifting"]
#         csv_file = csv.DictReader(readFile, fieldnames)
#         # header = csv_file[0]
#         coord_row = []
#         coordinates = []
#         try:
#             for row in csv_file:
#                 try:
#                     coord_row.append(float(row['x']))
#                     coord_row.append(float(row['y']))
#                     coordinates.append(coord_row)
#                     coord_row = []
#                 except ValueError:
#                     if row['x'] == 'width':
#                         building_width = float(row['y'])
#                     if row['x'] == 'length':
#                         building_length = float(row['y'])
#                     if row['x'] == 'nw height':
#                         building_height = float(row['y'])
#                     if row['x'] == 'ne height':
#                         if building_height != float(row['y']):
#                             sys.exit('building is not flat')
#                     if row['x'] == 'sw height':
#                         if building_height != float(row['y']):
#                             sys.exit('building is not flat')
#                     if row['x'] == 'se height':
#                         if building_height != float(row['y']):
#                             sys.exit('building is not flat')
#                     pass
#         except csv.Error as e:
#             sys.exit('file {}, line {}: {}'.format(
#                 filepath, csv_file.line_num, e))
#         return coordinates, building_width, building_length, building_height

def parse_input(filepath):
    with open(filepath, 'r') as readFile:
        csv_file = csv.DictReader(readFile)
        input_dict = {}
        inputs = []
        try:
            for row in csv_file:
                for key in row:
                    input_dict[key] = row[key]
                inputs.append(input_dict)
                input_dict = {}
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(
                filepath, csv_file.line_num, e))
        return inputs


def graph_polygons(building=None, zones=None, vortex_zones=None, arrays=None, max_x=0, max_y=0, show=True):
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
            ax.add_artist(PolygonPatch(building.polygon, alpha=.25))
        if zones:
            for zone in zones:
                ax.add_artist(PolygonPatch(
                    zones[zone], facecolor=colors[zone], alpha=.75))
                if zone == '1E':
                    ax.text(zones[zone].centroid.x,
                            zones[zone].centroid.y - 15, zone)
                else:
                    ax.text(zones[zone].centroid.x,
                            zones[zone].centroid.y, zone)

                # centroid represents the center of the polygon
        if arrays:
            for array in arrays:
                for panel in array.panel_list:
                    ax.add_artist(PolygonPatch(
                        panel.polygon, facecolor='#000050', alpha=.75))
                    # ax.text(panel.polygon.centroid.x,
                    #         panel.polygon.centroid.y, panel.identity, color='white')
        if vortex_zones:
            alt = False
            for zone in vortex_zones:
                if alt:
                    ax.add_artist(PolygonPatch(
                        vortex_zones[zone],  hatch='||', alpha=.2, fill=False, color='#000050'))
                else:
                    ax.add_artist(PolygonPatch(
                        # vortex_zones[zone],  facecolor='#ff6600', alpha=.5))
                        vortex_zones[zone],  hatch='--', alpha=.2, fill=False, color='#000050'))
                ax.text(vortex_zones[zone].centroid.x,
                        vortex_zones[zone].centroid.y, zone, color='white')
                alt = not alt
        # plt.show()
        plt.savefig("mygraph.png")
    return ax


def main():
    inputs = parse_input(input_filepath)
    building_coordinates = [[0.0, 0.0], [0.0, float(inputs[0]['w'])], [
        float(inputs[0]['l']), float(inputs[0]['w'])], [float(inputs[0]['l']), 0.0]]
    # building_coordinates, building_height = builder.calculate_building_coordinates(
    #     preset='rect')
    building_length = building_coordinates[2][0]
    building_width = building_coordinates[2][1]
    building_height = float(inputs[0]['z'])
    building = builder.Building(building_coordinates, building_length, building_width,
                                building_height, builder.build_polygons(building_coordinates))
    zones = builder.calculate_zones(building)
    vortex_zones = builder.calculate_vortex_zones(building)
    # array = panels.build_arrays(zones=zones, Lb=building_height, module_width=4, module_length=2, gap_length=1, rows=4,
    #                             columns=4, distance_left=10, distance_bottom=400, max_x=500, max_y=500)
    # array = panels.build_arrays(zones=zones, vortex_zones=vortex_zones, building_length=building_length, building_width=building_width, building_height=building_height, module_width=7, module_length=3, gap_length=0, rows=11,
    #                             columns=8, distance_left=440, distance_bottom=435, max_x=building_coordinates[2][0], max_y=building_coordinates[2][1])
    list_of_arrays = []
    for i in range(len(inputs)):
        # 440, 435
        distance_left = inputs[i]['array origin x']
        distance_bottom = inputs[i]['array origin y']
        panel_list = panels.build_arrays(zones=zones, vortex_zones=vortex_zones, building=building, module_width=float(inputs[i]['panel width']), module_length=float(inputs[i]['panel length']), gap_length=float(inputs[i]['array gap']), rows=int(inputs[i]['array rows']),
                                         columns=int(inputs[i]['array columns']), distance_left=float(distance_left), distance_bottom=float(distance_bottom))
        array = panels.Array(
            index=i, panel_list=panel_list, ns_gap=0, ew_gap=0)
        list_of_arrays.append(array)
    panels.generateReport(report=True, arrays=list_of_arrays,
                          parameter_dict=parameter_dict)
    graph_polygons(
        building=building, zones=zones, vortex_zones=None, arrays=list_of_arrays, max_x=building_coordinates[2][0], max_y=building_coordinates[2][1], show=True)
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
    # plt.show()


# class Interface(GridLayout):
#     pass


# class TutorialApp(App):
#     def build(self):
#         root_widget = Interface
#         return root_widget()

#     def process(self):
#         text = self.root.ids.height_input.text
#         print(text)

#     def check_positive(value):
#         if value < 0:
#             popup = Popup(content=Label(text='value must be positive'),
#                           size_hint=(None, None), size=(200, 200))
#             popup.open()


if __name__ == '__main__':
    main()
    # TutorialApp().run()
