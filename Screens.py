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

        label = pyglet.text.Label('Map Editing Mode', x = Window.window.width/2, y = Window.window.height - 10, anchor_x = 'center', anchor_y = 'center')
        label.draw()

