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
            self.velocity_x += self.speed * dt

        if self.key_handler[key.S]:
            self.velocity_x -= self.speed * dt

        if self.key_handler[key.A]:
            self.sprite.rotation -= self.rotation * dt

        if self.key_handler[key.D]:
            self.sprite.rotation += self.rotation * dt

        


###Initializing Objects####
Test_Player = Player(batch=Resources.player_batch)
