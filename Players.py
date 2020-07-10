import pyglet
import Resources
import Agents
import Objects
import Terrain


import math
from pyglet.window import key
from pyglet.window import mouse
import Functions
import random



class Player(Agents.Agents):

    def __init__(self,x=20,y=20,name=None,*args,**kwargs):
        super().__init__(img=Resources.spider_tank,*args,**kwargs)

        self.x = x
        self.y = y
        self.name = name

        self.sprite = pyglet.sprite.Sprite(img= Resources.spider_tank, batch = Resources.player_batch)

        #Player physics
        self.speed = 300.0
        self.mass = 1.0
        self.rotate_speed = 8
        self.rotation = 0

        #Player handling
        self.key_handler = Objects.global_key_handler
        self.mouse_handler = Objects.global_mouse_handler

        #Player's attributes
        self.lives = 3

        #Handles navigation
        self.navigation = False
        self.nav_path = []
        self.nav_index = 0

        #Action point restrictions
        self.move_points = 10
        self.max_move_points = 10

        #Player selected
        self.selected = False

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

        #Handles navigation
        if self.navigation == True:
            self.navigate_path(self.nav_path[self.nav_index],dt)

        #Keeps player on discrete pixels
        #self.x = int(round(self.x))
        #self.y = int(round(self.y))

        #If it's not the player's turn, then player has 0 points.
        if Objects.game_obj.player_turn == False:
            self.move_points = 0
        if Objects.game_obj.player_turn == True and self.move_points == 0:
            self.move_points = self.max_move_points





###Initializing Objects####
Test_Player1 = Player(x=150,y=150,batch=Resources.player_batch,name = 'Test Player 1')
Test_Player2 = Player(x=200,y=200,batch=Resources.player_batch, name = 'Test Player 2')
