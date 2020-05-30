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

camera = Objects.Camera(Window.window.width, Window.window.height)

Objects.game_obj.game_objects.extend([Players.Test_Player,Objects.game_mouse,Terrain.terrain_obj])


for cell in Terrain.terrain_obj.terrain_dict:
    if Terrain.terrain_obj.terrain_dict[cell].sprite.height != 10 or Terrain.terrain_obj.terrain_dict[cell].sprite.width != 10:
        print(cell)

print(Players.Test_Player.sprite.position)
print(Terrain.terrain_obj.terrain_dict[1,1].sprite.position)

Terrain.terrain_obj.construct_map('map1')


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
