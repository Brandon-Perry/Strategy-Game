#Import modules
import pyglet 
import math
import random
from pyglet.window import mouse

#Game files 
import Objects
import Resources
import Functions


###
#Game Window
window = pyglet.window.Window(1000,800)
window.push_handlers(Objects.global_key_handler)
window.push_handlers(Objects.global_mouse_handler)
###

Objects.terrain_obj.mountain_generator()
Objects.terrain_obj.hill_generator()
Objects.terrain_obj.swamp_generator()



def update(dt):
    Objects.game_obj.update(dt)

    #checks for collisions
    #Functions.collision_check(Objects.game_obj.game_objects)
   
    

@window.event
def on_mouse_motion(x, y, dx, dy):
    Objects.global_mouse_coordinates = x,y


@window.event
def on_draw():
    window.clear()
    
    Resources.terrain_batch.draw()
    Resources.player_batch.draw()
        
        
            

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update,1/120.0)
    pyglet.app.run()