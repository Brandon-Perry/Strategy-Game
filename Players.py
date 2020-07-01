import pyglet
import Resources
import Physical_Object
import Objects
import Terrain


import math
from pyglet.window import key
from pyglet.window import mouse
import Functions
import random



class Player(Physical_Object.PhyiscalObject):

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
        self.x = int(round(self.x))
        self.y = int(round(self.y))

        #if self.selected == True:
            #print('selected true')

    def navigate_path(self,point,dt):

        ####First rotate to the correct position

        #Find angle between current position and point

        #angle changed to negative because the way pyglet sets object orientation

        angle_to_point = -math.degrees(Functions.angle(point_1=(self.x,self.y),point_2=point))

        if math.fmod(self.rotation, 360) > angle_to_point:
            if math.fmod(self.rotation,360) - angle_to_point < self.rotate_speed:
                self.rotation = angle_to_point
            else:
                self.rotation -= self.rotate_speed

        if math.fmod(self.rotation, 360) < angle_to_point:
            if angle_to_point - math.fmod(self.rotation,360) < self.rotate_speed:
                self.rotation = angle_to_point
            else:
                self.rotation += self.rotate_speed

        #If player is at the correct angle, then go forward. If the point is within the vector-space, stop at the point instead.
        if math.fmod(self.rotation,360) == angle_to_point and (int(self.x),int(self.y)) != point:
            angle_radians = -math.radians(self.rotation)

            vector_x = math.cos(angle_radians) * self.speed * dt
            vector_y = math.sin(angle_radians) * self.speed * dt

            #print('vectorx',vector_x)
            #print('vectory',vector_y)

            if ((vector_x >= 0 and self.x + vector_x >= point[0]) or (vector_x <= 0 and self.x - vector_x <= point[0])) and \
                ((vector_y >= 0 and self.y + vector_y >= point[1]) or (vector_y <= 0 and self.y - vector_y <= point[1])):
                self.x = point[0]
                self.y = point[1]
                print('latched')
            else:

                self.x += vector_x
                self.y += vector_y
                self.x = int(round(self.x))
                self.y = int(round(self.y))
                print('point',point)
                print('position',self.x,self.y)

        #If the player is at the point, then either adjust the point to the next in list or stop navigation if at end
        if (int(self.x),int(self.y)) == point:

            if point == self.nav_path[-1]:
                self.nav_index = 0
                self.navigation = False
                print('here!')

            else:
                self.nav_index += 1


        #print('sprite position',self.sprite.position)
        #print('target position',point)
        #print('`````````')

    def return_player_cell(self):

        for coord in Terrain.terrain_obj.terrain_dict:

            cell = Terrain.terrain_obj.terrain_dict[coord]

            if cell.sprite.x - cell.sprite.width/2 < self.x < cell.sprite.x + cell.sprite.width/2 and \
                    cell.sprite.y - cell.sprite.height/2 < self.y < cell.sprite.y + cell.sprite.height/2:

                    return coord
###Initializing Objects####
Test_Player1 = Player(batch=Resources.player_batch,name = 'Test Player 1')
Test_Player2 = Player(x=50,y=50,batch=Resources.player_batch, name = 'Test Player 2')
