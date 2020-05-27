import pyglet
import Resources
import Functions


import math
from pyglet.window import key
from pyglet.window import mouse
import random




class PhyiscalObject(object):
    
    def __init__(self, x=0.0, y=0.0, *args,**kwargs):
        self.sprite = pyglet.sprite.Sprite(*args, **kwargs)
        
        #Location of object in world
        self.x = x
        self.y = y

        #Velocity
        self.velocity_x = 0.0
        self.velocity_y = 0.0

        #Alive status
        self.dead = False


    def update(self,dt, camera):
        #Velocity and how it affects movement (dt is frame)
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        camera.update_sprite(self.sprite, self.x, self.y)
    

