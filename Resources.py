import pyglet

#sets pyglet resource path
pyglet.resource.path = ['resources']
pyglet.resource.reindex()




#Ship images
test_player = pyglet.resource.image('Player.png')


#Terrain images
grass_img = pyglet.resource.image('Grass.png')
mountain_img = pyglet.resource.image('Mountain.png')
hill_img = pyglet.resource.image('Hill.png')
swamp_img = pyglet.resource.image('Swamp.png')








#Centers images
def center_image(image):
    #sets an image's anchor point to its center
    
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

def animation_center(anim):
    for f in anim.frames:
        f.image.anchor_x = f.image.width // 2
        f.image.anchor_y = f.image.height // 2


center_image(test_player)
center_image(grass_img)
center_image(mountain_img)
center_image(hill_img)
center_image(swamp_img)



#Batches

player_batch = pyglet.graphics.Batch()
terrain_batch = pyglet.graphics.Batch()