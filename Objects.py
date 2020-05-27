import pyglet
import Resources
import Functions


import math
from pyglet.window import key
from pyglet.window import mouse
import random



global_key_handler = key.KeyStateHandler()
global_mouse_handler = mouse.MouseStateHandler()


class Camera(object):
    def __init__(self, screen_width, screen_height):
        self.x = self.y = 0.0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.zoom = 1.0

        

    def zoom_in(self):
        self.zoom += .1

    def zoom_out(self):
        self.zoom -= .1


    def pan(self, offset_x, offset_y):
        self.x += offset_x
        self.y += offset_y
    

    def update_sprite(self, sprite, world_x, world_y):
        sprite.x = (world_x - self.x) * self.zoom
        sprite.y = (world_y - self.y) * self.zoom
        sprite.scale = self.zoom




class GamePlay(object):

    def __init__(self, x=0, y=0, *args,**kwargs):

        self.game_objects = []

        #Handles key input
        self.key_handler = global_key_handler
        self.mouse_handler = global_mouse_handler
        self.enter_key_pressed = False #Makes sure there's only one action per press
        self.tab_key_pressed = False #Makes sure there's only one action per press


    def update(self,dt, camera):

        #Updates all the objects in the game_objects list
        for obj in self.game_objects:
            obj.update(dt, camera)

        #Checks for dead objects and removes them
        for to_remove in [obj for obj in game_obj.game_objects if obj.dead]:
            self.game_objects.remove(to_remove)
            del to_remove

        #Handles Camera zooming and panning
        #if self.mouse_handler[button.LEFT]:
            #camera.zoom_in()

        if self.key_handler[key.TAB]:
            camera.zoom_out()

        if self.key_handler[key.W]:
            camera.pan(0,10)

        if self.key_handler[key.A]:
            camera.pan(-10,0)
        
        if self.key_handler[key.D]:
            camera.pan(10,0)

        if self.key_handler[key.S]:
            camera.pan(0,-10)



class Mouse(object):

    def __init__(self, x=0, y=0, *args,**kwargs):

        #Cursor location
        self.x = x
        self.y = y

        #Mouse states
        self.scroll = 1

        self.mouse_handler = global_mouse_handler

        self.dead = False

        self.outside_right = False
        self.outside_left = False
        self.outside_up = False
        self.outside_down = False


    def update(self,dt,camera):

        #Translates self zoom into zooming for camera
        camera.zoom = self.scroll

        #If the mouse is outside the window, then have the camera pan

        if self.outside_down:
            camera.pan(0,1)

        if self.outside_right:
            camera.pan(-1,0)
        
        if self.outside_left:
            camera.pan(1,0)

        if self.outside_up:
            camera.pan(0,-1)
        



#Initiating Objects


game_mouse = Mouse(batch=Resources.player_batch)

game_obj = GamePlay(x=0,y=0)



