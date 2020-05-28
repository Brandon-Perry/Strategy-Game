import pyglet
import Resources
import Functions

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


        
        self.sprite = pyglet.sprite.Sprite(img = self.load_checker_sprite(), batch = batch, *args, **kwargs)




    def load_checker_sprite(self):


        checker_img = pyglet.image.CheckerImagePattern(color1=(150, 150, 150, 255), color2=(200, 200, 200, 255))
        sprite_img = checker_img.create_image(self.dimensions[0],self.dimensions[1])

        Resources.center_image(sprite_img)



        return sprite_img

        
        
        


    def update(self,dt,camera):
 
        camera.update_sprite(self.sprite, self.x, self.y)

        
        



###Initializes Object###
terrain_obj = Terrain(x = 400, y = 300, dimensions = (1000,1000), unit_size=10, batch = Resources.terrain_batch)