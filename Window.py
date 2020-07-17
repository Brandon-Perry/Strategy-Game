import pyglet
from pyglet.window import key,mouse
import Objects
import Functions
import Terrain
import Objects
import Players
import Enemy
import math


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

    if (button & mouse.LEFT) and Objects.game_obj.game_state == 'Map Editor':
        Terrain.terrain_obj.map_editor_function(x,y)

    #Run Dijskstra search
    if (button & mouse.LEFT) and Objects.game_obj.game_state == 'Main':
        #print('left selected')
        #if player is selected agent, run djikstra or fire weapon if click is on opposing side
        for player in [obj for obj in Objects.game_obj.game_objects if obj.__class__ == Players.Player or obj.__class__ == Enemy.Enemy]:

            if player.selected == True:

                #Check if click interlaps with opposing side sprite
                for agent in [obj for obj in Objects.game_obj.game_objects if (obj.__class__ == Players.Player or obj.__class__ == Enemy.Enemy)\
                    and obj.selected == False]:
                    if agent.return_if_x_y_in_sprite_loc(x,y):
                        player.attack_target(agent)
                        return #break code here if true


                #If not, then navigate to cell

                #print('got to this point')
                player.handle_navigation(x,y)


    #Select player
    if (button & mouse.RIGHT) and Objects.game_obj.game_state == 'Main':
        print('right selected')
        #Runs through players and makes player.selected = True if within mouse coordinates
        for player in [obj for obj in Objects.game_obj.game_objects if obj.__class__ == Players.Player or obj.__class__ == Enemy.Enemy]:

            Functions.player_selector(x,y,player)

        #highlights which cells the selected player can move to
        selected_player = [obj for obj in Objects.game_obj.game_objects if (obj.__class__ == Players.Player or obj.__class__ == Enemy.Enemy)\
            and obj.selected == True]
        available_coords = Terrain.terrain_obj.move_distance_calc(selected_player[0])
        Terrain.terrain_obj.reset_highlighted_terrain()
        Terrain.terrain_obj.highlight_terrain_func(available_coords)




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


@window.event
def on_key_release(symbol, modifiers):

    if Objects.game_obj.game_state == 'Map Editor':

        if modifiers & key.MOD_SHIFT:

            #For saving map states
            if symbol == key._0:
                Terrain.terrain_obj.generate_map_data('0')

            elif symbol == key._1:
                Terrain.terrain_obj.generate_map_data('1')

            elif symbol == key._2:
                Terrain.terrain_obj.generate_map_data('2')

            elif symbol == key._3:
                Terrain.terrain_obj.generate_map_data('3')

            elif symbol == key._4:
                Terrain.terrain_obj.generate_map_data('4')

            elif symbol == key._5:
                Terrain.terrain_obj.generate_map_data('5')

            elif symbol == key._6:
                Terrain.terrain_obj.generate_map_data('6')

            elif symbol == key._7:
                Terrain.terrain_obj.generate_map_data('7')

            elif symbol == key._8:
                Terrain.terrain_obj.generate_map_data('8')

            elif symbol == key._9:
                Terrain.terrain_obj.generate_map_data('9')

        #For loading maps
        if symbol == key._0:
            Terrain.terrain_obj.construct_map('0')

        elif symbol == key._1:
            Terrain.terrain_obj.construct_map('1')

        elif symbol == key._2:
            Terrain.terrain_obj.construct_map('2')

        elif symbol == key._3:
            Terrain.terrain_obj.construct_map('3')

        elif symbol == key._4:
            Terrain.terrain_obj.construct_map('4')

        elif symbol == key._5:
            Terrain.terrain_obj.construct_map('5')

        elif symbol == key._6:
            Terrain.terrain_obj.construct_map('6')

        elif symbol == key._7:
            Terrain.terrain_obj.construct_map('7')

        elif symbol == key._8:
            Terrain.terrain_obj.construct_map('8')

        elif symbol == key._9:
            Terrain.terrain_obj.construct_map('9')
