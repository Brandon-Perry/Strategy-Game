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
import Window
import Screens


###
#Game Window

###

camera = Objects.Camera(Window.window.width, Window.window.height)

Objects.game_obj.game_objects.extend([Players.Test_Player,Objects.game_mouse,Terrain.terrain_obj])




def update(dt):

   Objects.game_obj.update(dt,camera)



@Window.window.event
def on_draw():

    Screens.screen_display(Objects.game_obj.game_state)




if __name__ == "__main__":
    pyglet.clock.schedule_interval(update,1/120.0)
    pyglet.app.run()
