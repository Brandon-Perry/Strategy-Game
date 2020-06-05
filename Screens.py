import pyglet
import Window
import Resources

def screen_display(input):

    if input == 'Main':

        Window.window.clear()
            
        Resources.terrain_batch.draw()

        Resources.player_batch.draw()

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
