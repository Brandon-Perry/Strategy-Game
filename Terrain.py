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

        #Runs init_terrain upon initialization
        self.init_terrain()

           
        
    def update(self,dt,camera):
 
        #camera.update_sprite(self.sprite, self.x, self.y)
        pass

    
    def init_terrain(self):
        #Initializes a grid of grass cells the size of the specified dimensions

        for dim_x in range(0,self.dimensions[0]):

            for dim_y in range(0,self.dimensions[1]):

                cell_x = self.unit_size * dim_x
                cell_y = self.unit_size * dim_y

                new_cell = Terrain_Unit(x = cell_x, y = cell_y, coord = (dim_x+1, dim_y+1), size = self.unit_size, terrain_type = 'Grass')
                Objects.game_obj.game_objects.append(new_cell)
                self.terrain_dict[new_cell.coord] = new_cell 


    def replace_cell(self,location,type):

        self.terrain_dict[location].terrain_type = type
        self.terrain_dict[location].sprite.image = self.terrain_dict[location].init_cell()


    def generate_map_data(self,map_num):

        map_file = open("Map_Databases/" + map_num + ".txt","w")

        #cell_list = []

        for coord in self.terrain_dict:

            terrain_type = self.terrain_dict[coord].terrain_type

            if coord[1] == 1 and coord[0] != 1:
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
            
            print((sym))

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

        self.sprite.image.height = self.sprite.image.width = self.size


    def init_cell(self):

        if self.terrain_type == 'Grass': 
            self.terrain_mov_mod = 1

            return Resources.grass_img

        if self.terrain_type == 'Hill':
            self.terrain_mov_mod = 3

            return Resources.hill_img

        if self.terrain_type =='Mountain':
            self.terrain_mov_mod = 1000

            return Resources.mountain_img

        if self.terrain_type == 'Swamp':
            self.terrain_mov_mod = 2

            return Resources.swamp_img

    def update(self,dt,camera):
        camera.update_sprite(self.sprite,self.x,self.y)


###Initializes Object###
terrain_obj = Terrain(dimensions = (20,20), unit_size=10, batch = Resources.terrain_batch)