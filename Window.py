import pyglet
from pyglet.window import key,mouse
import Objects
import Terrain


window = pyglet.window.Window(500,500)
window.push_handlers(Objects.global_key_handler)
window.push_handlers(Objects.global_mouse_handler)


#Mouse on_event functions

@window.event
def on_mouse_motion(x,y,dx,dy):
    
    Objects.game_mouse.x = x
    Objects.game_mouse.y = y


@window.event
def on_mouse_press(x,y,button,modifiers):

    if mouse.LEFT and Objects.game_obj.map_mode == 'Map Editor':
        Terrain.terrain_obj.map_editor_function(x,y)
    

@window.event
def on_mouse_scroll(x,y,scroll_x,scroll_y):

    Objects.game_mouse.scroll += (scroll_y/10)
        

@window.event
def on_mouse_leave(x,y):

    if x > window.width:
        Objects.game_mouse.outside_right = True
    
    if x < 0:
        Objects.game_mouse.outside_left = True

    if y > window.height:
        Objects.game_mouse.outside_down = True

    if y < 0:
        Objects.game_mouse.outside_up = True


@window.event
def on_mouse_enter(x,y):

    Objects.game_mouse.outside_down = False
    Objects.game_mouse.outside_left = False
    Objects.game_mouse.outside_right = False 
    Objects.game_mouse.outside_up = False