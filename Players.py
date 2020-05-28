import pyglet
import Resources
import Physical_Object
import Objects


import math
from pyglet.window import key
from pyglet.window import mouse
import Functions
import random


  
class Player(Physical_Object.PhyiscalObject):

    def __init__(self,x=400,y=100.0,*args,**kwargs):
        super().__init__(img=Resources.spider_tank,*args,**kwargs)

        self.x = x
        self.y = y

        self.sprite = pyglet.sprite.Sprite(img= Resources.spider_tank, batch = Resources.player_batch)

        #Ship physics
        self.speed = 300.0
        self.mass = 1.0
        self.rotate_speed = 125
        self.rotation = 0
        
        #Ship handling
        self.key_handler = Objects.global_key_handler
        self.mouse_handler = Objects.global_mouse_handler

        #Player's attributes
        self.lives = 3

    def update(self,dt, camera):

        super(Player,self).update(dt, camera)
        self.sprite.rotation = self.rotation

        if self.key_handler[key.W]:
            
            angle_radians = -math.radians(self.rotation)

            vector_x = math.cos(angle_radians) * self.speed * dt
            vector_y = math.sin(angle_radians) * self.speed * dt
            
            self.x += vector_x
            self.y += vector_y

        if self.key_handler[key.S]:
            angle_radians = -math.radians(self.rotation)

            vector_x = math.cos(angle_radians) * self.speed * dt
            vector_y = math.sin(angle_radians) * self.speed * dt
            
            self.x -= vector_x
            self.y -= vector_y

        if self.key_handler[key.A]:
            self.rotation -= self.rotate_speed * dt

        if self.key_handler[key.D]:
            self.rotation += self.rotate_speed * dt

        


###Initializing Objects####
Test_Player = Player(batch=Resources.player_batch)
