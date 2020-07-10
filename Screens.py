import pyglet
import Window
import Resources
import Objects

def screen_display(input):

    if input == 'Main':

        Window.window.clear()

        Resources.terrain_batch.draw()

        Resources.player_batch.draw()

        Resources.enemy_batch.draw()

        Resources.effects_batch.draw()

        if Objects.game_obj.player_turn == True:
            turn_label = pyglet.text.Label('Players Turn', x = Window.window.width/2, y = Window.window.height - 10, anchor_x = 'center',\
                 anchor_y = 'center')
        else:
            turn_label = pyglet.text.Label('Enemys Turn', x = Window.window.width/2, y = Window.window.height - 10, anchor_x = 'center',\
                 anchor_y = 'center')

        turn_label.draw()

    elif input == 'Map Editor':

        Window.window.clear()
        Resources.terrain_batch.draw()

        map_label = pyglet.text.Label('Map Editing Mode', x = Window.window.width/2, y = Window.window.height - 10, anchor_x = 'center', anchor_y = 'center')
        map_label.draw()

        instructions_label = pyglet.text.Label('Press a num key to load a map. Press SHIFT + num to save current map to that key',\
                    x = Window.window.width/2, y = map_label.y - 15, anchor_x = 'center', anchor_y = 'center')
        instructions_label.draw()

class Screen(object):

    def __init__(self):

        self.batch_dictionary = []

        self.label_dictionary = []
