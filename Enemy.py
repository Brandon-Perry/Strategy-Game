#Import modules
import pyglet
import math
import random
from pyglet.window import mouse

#Game files
import Objects
import Players
import Terrain
import Resources
import Functions
import math
import Agents


class Enemy(Agents.Agents):

    def __init__(self, x=0, y=0, name=None, *args, **kwargs):

        self.x = x
        self.y = y

        super().__init__(img=Resources.alien_tank,*args,**kwargs)

        self.x = x
        self.y = y
        self.name = name

        self.sprite = pyglet.sprite.Sprite(img= Resources.alien_tank, batch = Resources.enemy_batch)
        self.sprite.scale = .1

        #Enemy physics
        self.speed = 300.0
        self.mass = 1.0
        self.rotate_speed = 8
        self.rotation = 0

        #Enemy's attributes
        self.lives = 3

        #Handles navigation
        self.navigation = False
        self.nav_path = []
        self.nav_index = 0

        #Action point restrictions
        self.move_points = 10
        self.max_move_points = 10

        #Enemy selected
        self.selected = False

    def update(self,dt, camera):

        super(Enemy,self).update(dt, camera)
        self.sprite.rotation = self.rotation

        #Handles navigation
        if self.navigation == True:
            self.navigate_path(self.nav_path[self.nav_index],dt)

        #If it's the player's turn, then enemy has 0 points.
        if Objects.game_obj.player_turn == True:
            self.move_points = 0
        if Objects.game_obj.player_turn == False and self.move_points == 0:
            self.move_points = self.max_move_points



#Initializing Object
Enemy1 = Enemy(x=400,y=400,name='Enemy1',batch=Resources.enemy_batch)
