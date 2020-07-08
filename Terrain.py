import pyglet
import Resources
import Functions
import Objects

import math
from pyglet.window import key
from pyglet.window import mouse
import random



class Terrain(object):

    def __init__(self, x=0, y=0, dimensions=(0,0), unit_size=0, batch = None, *args, **kwargs):

        self.x = x
        self.y = y

        self.dimensions = dimensions

        self.unit_size = unit_size

        self.dead = False

        self.terrain_dict = {}

        self.highlighted_terrain = {} #contains coord and original terrian_type

        #Runs init_terrain upon initialization
        self.init_terrain()

        self.camera_position = None
        self.camera_zoom = 1

        #Handles keys
        self.key_handler = Objects.global_key_handler


    def update(self,dt,camera):

        #camera.update_sprite(self.sprite, self.x, self.y)
        self.camera_position = (camera.x,camera.y)
        self.camera_position = camera.zoom

        #Map Saving and loading handled in Window.py


    def init_terrain(self):
        #Initializes a grid of grass cells the size of the specified dimensions

        for dim_x in range(0,self.dimensions[0]):

            for dim_y in range(0,self.dimensions[1]):

                cell_x = self.unit_size * dim_x
                cell_y = self.unit_size * dim_y

                new_cell = Terrain_Unit(x = cell_x, y = cell_y, coord = (dim_x+1, dim_y+1), size = self.unit_size, terrain_type = 'Grass')
                Objects.game_obj.game_objects.append(new_cell)
                self.terrain_dict[new_cell.coord] = new_cell

    ####Functions for map editing

    def replace_cell(self,location,t_type):



        self.terrain_dict[location].terrain_type = t_type

        self.terrain_dict[location].sprite.image = self.terrain_dict[location].init_cell()

        self.terrain_dict[location].set_size()


    def map_editor_function(self,x,y):



        for coord in self.terrain_dict:
            cell = self.terrain_dict[coord]

            if cell.sprite.x - cell.sprite.width/2 < x < cell.sprite.x + cell.sprite.width/2 and \
                cell.sprite.y - cell.sprite.height/2 < y < cell.sprite.y + cell.sprite.height/2:

                if cell.terrain_type == 'Grass':
                    self.replace_cell(coord,'Hill')
                elif cell.terrain_type == 'Hill':
                    self.replace_cell(coord,'Swamp')
                elif cell.terrain_type == 'Swamp':
                    self.replace_cell(coord,'Mountain')
                elif cell.terrain_type == 'Mountain':
                    self.replace_cell(coord,'Grass')



                break

    ####Functions for saving and loading maps
    def generate_map_data(self,map_num):

        map_file = open("Map_Databases/" + map_num + ".txt","w")


        cell_count_x = range(1,self.dimensions[0]+1)
        cell_count_y = range(1,self.dimensions[1]+1)

        for x in cell_count_x:

            for y in cell_count_y:


                terrain_type = self.terrain_dict[(y,x)].terrain_type


                if y == 1 and x != 1:
                    map_file.write('-\n')

                if terrain_type == 'Grass':
                    map_file.write('0')
                elif terrain_type == 'Swamp':
                    map_file.write('1')
                elif terrain_type == 'Hill':
                    map_file.write('2')
                elif terrain_type == 'Mountain':
                    map_file.write('3')


    def construct_map(self,map_num):

        #First, delete current map


        self.terrain_dict.clear()
        for cell in [obj for obj in Objects.game_obj.game_objects if obj.__class__ == Terrain_Unit]:
            Objects.game_obj.game_objects.remove(cell)




        map_file = open("Map_Databases/" + map_num + ".txt","r")

        reconstruction_list = []

        x_coord = 1
        y_coord = 1

        for sym in map_file.read():

            if sym == '-':
                y_coord += 1
                x_coord = 1

            else:

                if sym == '0':
                    reconstruction_list.append(((x_coord,y_coord),'Grass'))
                    x_coord += 1
                elif sym == '1':
                    reconstruction_list.append(((x_coord,y_coord),'Swamp'))
                    x_coord += 1
                elif sym == '2':
                    reconstruction_list.append(((x_coord,y_coord),'Hill'))
                    x_coord += 1
                elif sym == '3':
                    reconstruction_list.append(((x_coord,y_coord),'Mountain'))
                    x_coord += 1
                else:
                    pass

        for cell in reconstruction_list:
            coord = cell[0]
            x_coord = coord[0]
            y_coord = coord[1]
            terrain_string = cell[1]

            x_pos = self.unit_size * x_coord-1
            y_pos = self.unit_size * y_coord-1

            new_cell = Terrain_Unit(x = x_pos, y = y_pos, coord = (x_coord,y_coord), terrain_type=terrain_string, size=self.unit_size)
            self.terrain_dict[new_cell.coord] = new_cell
            Objects.game_obj.game_objects.append(new_cell)

    ####Functions for navigation
    def return_sprite_index(self,x,y):

        for coord in self.terrain_dict:

            cell = self.terrain_dict[coord]

            if cell.sprite.x - cell.sprite.width/2 < x < cell.sprite.x + cell.sprite.width/2 and \
                    cell.sprite.y - cell.sprite.height/2 < y < cell.sprite.y + cell.sprite.height/2:

                    return coord

    def return_cell_index(self,x,y):

        for coord in self.terrain_dict:

            cell = self.terrain_dict[coord]

            if cell.x - cell.size/2 < x < cell.x + cell.size/2 and \
                    cell.y - cell.size/2 < y < cell.y + cell.size/2:

                    return coord


    ####Functions for Dijkstra search
    def return_neighbors(self,coord):

        x = coord[0]
        y = coord[1]

        neighbor_list = [(x+1,y),(x-1,y),(x,y+1),(x,y-1),(x+1,y+1),(x-1,y-1),(x+1,y-1),(x-1,y+1)]

        return neighbor_list


    def Dijkstra_algorithm(self,start_node,end_node):

        #for testing


        already_searched = []

        shortest_path_value = {}

        previous_node = {}

        search_que = []

        #Initial sets all distances as very large, start node as zero
        for node in self.terrain_dict:
            shortest_path_value[node] = math.inf

        shortest_path_value.update({start_node:0})

        current_node = start_node

        #Begins search for the shortest path
        while True:

            neighbors = self.return_neighbors(current_node)
            #print('neighbors',neighbors)

            current_cell = self.terrain_dict[current_node]
            #print('current node',current_node)

            #First find the distance from the current node to its neighbor node
            for coord in [loc for loc in neighbors if loc not in already_searched or\
                self.terrain_dict[loc].terrain_type != 'Mountain']:
                try:
                    #print('coord in find distance from current node to neighbor node',coord)
                    neighbor_cell = self.terrain_dict[coord]

                    neighbor_node_distance = Functions.distance((current_cell.x,current_cell.y),(neighbor_cell.x,neighbor_cell.y))

                    neighbor_node_distance *= neighbor_cell.terrain_mov_mod

                    #Adds to total distance and compares to current shortest distance, changes if smaller

                    distance_to_start = shortest_path_value[current_node]

                    total_distance = distance_to_start + neighbor_node_distance
                    #print('total distance',total_distance)

                    if total_distance < shortest_path_value[coord]:
                        shortest_path_value.update({coord:total_distance})
                        #print('shortest path for this node', coord, shortest_path_value[coord])
                        previous_node.update({coord:current_node})
                        #print('previous nodes',previous_node)

                        #adds to search que if not already in the list
                        if coord not in search_que:
                            search_que.append(coord)
                        else:
                            pass
                except:
                    pass
            #After neighbors have been updated, sort priority que, update searched list, and do again unless the end has been reached

            if current_node == end_node:
                #print('found the end node',end_node)
                path_list = [end_node]
                search_node = current_node
                while True:
                    path_list.append(previous_node[search_node])
                    #print('path list',path_list)

                    if previous_node[search_node] == start_node:
                        path_list = path_list[::-1]
                        #print(path_list)
                        #print('pathlist before straightner function',path_list)
                        path_list = Functions.path_straightner(path_list)
                        #print(path_list)
                        #print('final path list',path_list)
                        return path_list
                    else:
                        search_node = previous_node[search_node]




            already_searched.append(current_node)

            #print('already searched',already_searched)

            current_node = search_que[0]

            for node in search_que:
                if shortest_path_value[node] < shortest_path_value[node]:
                    current_node = node
            #print('new current node',current_node)


            search_que.remove(current_node)
            #print('search que',search_que)


            if end_node in search_que:
                current_node = end_node

            #print("``````")

    def move_distance_calc(self,entity):

        available_cells = []

        search_que = []

        start_node = self.return_cell_index(entity.x,entity.y)

        already_searched = [start_node]

        #print(start_node)
        #print(entity.x,entity.y)

        beginning_neighbors = Functions.find_neighbors(start_node)

        for node in beginning_neighbors:
            if node in self.terrain_dict:
                search_que.append(node)

        current_node = search_que[0]


        while True:

            print('current node',current_node)

            if self.terrain_dict[current_node].terrain_mov_mod != math.inf:

                sum_distance = 0

                path_list = self.Dijkstra_algorithm(start_node,current_node)

                for unit in path_list:

                    if unit == path_list[0]:
                        continue

                    previous_index = path_list.index(unit) - 1

                    sum_distance += (Functions.distance(point_1=(unit),point_2=(path_list[previous_index])) * self.terrain_dict[unit].terrain_mov_mod)

                if sum_distance <= entity.move_points:
                    available_cells.append(current_node)
                    new_neighbors = Functions.find_neighbors(current_node)
                    search_que.extend([x for x in new_neighbors if x in self.terrain_dict and x not in already_searched and x not in search_que])
                    #print('sum distance',current_node,sum_distance)
                else:
                    #print('too far',current_node)
                    #self.replace_cell(current_node,'Yellow')
                    pass
            else:
                #self.replace_cell(current_node,'Yellow')
                pass

            already_searched.append(current_node)
            search_que.remove(current_node)

            if len(search_que) == 0:
                #print(available_cells)
                return available_cells

            current_node = search_que[0]
            #print(current_node)

    def highlight_terrain_func(self,coord_list):
        #First add coords and original terrain types to dictionary
        for coord in coord_list:
            self.highlighted_terrain[coord] = self.terrain_dict[coord].terrain_type

        #Then, go through and highlight cells
        for coord in coord_list:
            self.replace_cell(coord,'Yellow')

    def reset_highlighted_terrain(self):
        for coord in self.highlighted_terrain:
            self.replace_cell(coord,self.highlighted_terrain[coord])

        self.highlighted_terrain = {}







    def return_player_cell(self,player_object):

        (player_x,player_y) = (player_object.x,player_object.y)

        for coord in self.terrain_dict:

            cell = self.terrain_dict[coord]

            if cell.x - cell.size/2 < player_x < cell.x + cell.size/2 and \
                        cell.y - cell.size/2 < player_y < cell.y + cell.size/2:

                        return coord

    def return_cell_position(self,cell):
        x = self.terrain_dict[cell].x
        y = self.terrain_dict[cell].y

        return x,y

    def return_list_cell_positions(self,cell_list):

        pos_list = []

        for cell in cell_list:
            new_entry = self.return_cell_position(cell)
            pos_list.append(new_entry)

        return pos_list

    def color_path(self,path):

        for cell in path:

            self.replace_cell(cell,'Black')


class Terrain_Unit(object):

    def __init__(self, x = 0, y = 0, coord = (0,0), terrain_type = None, size = 0, *args, **kwargs):

        self.x = x
        self.y = y

        self.coord = coord

        self.terrain_type = terrain_type

        self.terrain_mov_mod = 0

        self.size = size

        self.dead = False

        self.sprite = pyglet.sprite.Sprite(img = self.init_cell(), x = self.x, y = self.y, batch = Resources.terrain_batch)

        self.set_size()



    def init_cell(self):

        if self.terrain_type == 'Grass':
            self.terrain_mov_mod = 1

            return Resources.grass_img

        if self.terrain_type == 'Hill':
            self.terrain_mov_mod = 3

            return Resources.hill_img

        if self.terrain_type =='Mountain':
            self.terrain_mov_mod = math.inf

            return Resources.mountain_img

        if self.terrain_type == 'Swamp':
            self.terrain_mov_mod = 2

            return Resources.swamp_img

        if self.terrain_type == 'Black':
            return Resources.black_img

        if self.terrain_type == 'Yellow':
            return Resources.yellow_img

    def set_size(self):

        self.sprite.image.height = self.sprite.image.width = self.size
        Resources.center_image(self.sprite.image)

    def update(self,dt,camera):
        camera.update_sprite(self.sprite,self.x,self.y)


###Initializes Object###
terrain_obj = Terrain(dimensions = (50,50), unit_size=10, batch = Resources.terrain_batch)
