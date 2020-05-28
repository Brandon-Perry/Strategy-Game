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



###
#Game Window

###

camera = Objects.Camera(1000, 800)

Objects.game_obj.game_objects.extend([Players.Test_Player,Objects.game_mouse,Terrain.terrain_obj])



def update(dt):
    
   Objects.game_obj.update(dt,camera)
    



@Window.window.event
def on_draw():
    Window.window.clear()
    
    Resources.terrain_batch.draw()

    Resources.player_batch.draw()
    



if __name__ == "__main__":
    pyglet.clock.schedule_interval(update,1/120.0)
    pyglet.app.run()
