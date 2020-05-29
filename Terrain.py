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

                cell_y = self.unit_size * dim_x
                cell_x = self.unit_size * dim_y

                new_cell = Terrain_Unit(x = cell_x, y = cell_y, coord = (dim_x+1, dim_y+1), size = self.unit_size, terrain_type = 'Grass')
                Objects.game_obj.game_objects.append(new_cell)
                self.terrain_dict[new_cell.coord] = new_cell 


        for coord in self.terrain_dict:
            print(coord,self.terrain_dict[coord].sprite.x,self.terrain_dict[coord].sprite.y)
                



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
terrain_obj = Terrain(x = 400, y = 300, dimensions = (20,20), unit_size=20, batch = Resources.terrain_batch)