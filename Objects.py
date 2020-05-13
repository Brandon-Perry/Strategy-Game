import pyglet
import Resources
import math
from pyglet.window import key
import Functions
import random

global_key_handler = key.KeyStateHandler()

class Camera(object):
    def __init__(self, screen_width, screen_height):
        self.x = self.y = 0.0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.zoom = 1.0

    def zoom_in(self):
        self.zoom *= 2

    def zoom_out(self):
        self.zoom /= 2

    def pan(self, offset_x, offset_y):
        self.x += offset_x
        self.y += offset_y

    def update_sprite(self, sprite, world_x, world_y):
        sprite.x = (world_x - self.x) * self.zoom
        sprite.y = (world_y - self.y) * self.zoom
        sprite.scale = self.zoom


class PhyiscalObject(object):
    
    def __init__(self, x=0.0, y=0.0, *args,**kwargs):
        self.sprite = pyglet.sprite.Sprite(*args, **kwargs)
        
        #Location of object in world
        self.x = x
        self.y = y

        #Velocity
        self.velocity_x = 0.0
        self.velocity_y = 0.0

        #Gravity
        #self.gravity = 5

        #Is object alive?
        #self.dead = False
        #self.destructable = True

        #Objects to be added to game, used for player and alien bullets
        #self.new_objects = []

        self.dead = False


    def update(self,dt, camera):
        #Velocity and how it affects movement (dt is frame)
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        camera.update_sprite(self.sprite, self.x, self.y)
        #self.check_bounds()

    def check_bounds(self):
        #Once the map size has been established, can use this function
        #if item reaches the edges of the map, then it stops them from going any further
        min_x = self.width / 2
        min_y = self.height / 2
        max_x = 800 - self.width / 2
        max_y = 600 - self.height / 2
        if self.x <= min_x:
            self.x = min_x
            self.velocity_x = 0
        elif self.x >= max_x:
            self.x = max_x
            self.velocity_x = 0
        if self.y <= min_y:
            self.y = min_y
            self.velocity_y = 0
        elif self.y >= max_y:
            self.y = max_y
            self.velocity_y = 0
    
    def collides_with(self,other_object):
        

        #Calculates collision distance 
        collision_distance = self.width/2 + other_object.width/2
        actual_distance = Functions.distance(self.position,other_object.position)
        return (actual_distance <= collision_distance)
    
    def handle_collision_with(self,other_object): 
        
        pass

        
  

class Player(PhyiscalObject):

    def __init__(self,x=400,y=100.0,*args,**kwargs):
        super().__init__(img=Resources.test_player,*args,**kwargs)

        self.x = x
        self.y = y

        #Ship physics
        self.thrust = 100.0
        self.mass = 1.0
        self.rotate_speed = 75.0
        self.rotation = 0
        
        #Ship handling
        self.key_handler = global_key_handler

        #Player's attributes
        self.lives = 3

    def update(self,dt, camera):

        super(Player,self).update(dt, camera)
        self.thrusters(dt)
        self.sprite.rotation = self.rotation



    def thrusters(self,dt):
        #Rotation
        if self.key_handler[key.LEFT]:
            self.rotation -= self.rotate_speed * dt

        if self.key_handler[key.RIGHT]:
            self.rotation += self.rotate_speed * dt

        #Thrust and deceleration
        if self.key_handler[key.UP]:
            angle_radians = -math.radians(self.rotation)
            force_x = math.cos(angle_radians) * self.thrust * dt
            force_y = math.sin(angle_radians) * self.thrust * dt
     
            self.velocity_x += force_x
            self.velocity_y += force_y

        if self.key_handler[key.DOWN]:
            angle_radians = -math.radians(self.rotation)
            force_x = math.cos(angle_radians) * self.thrust * dt
            force_y = math.sin(angle_radians) * self.thrust * dt
            self.velocity_x -= force_x
            self.velocity_y -= force_y


    

class GamePlay(pyglet.sprite.Sprite):

    def __init__(self, x=0, y=0, *args,**kwargs):

        self.game_objects = []

        #Handles key input
        self.key_handler = global_key_handler
        self.enter_key_pressed = False #Makes sure there's only one action per press
        self.tab_key_pressed = False #Makes sure there's only one action per press


    def update(self,dt, camera):

        #Updates all the objects in the game_objects list
        for obj in self.game_objects:
            obj.update(dt, camera)

        #Checks for dead objects and removes them
        for to_remove in [obj for obj in game_obj.game_objects if obj.dead]:
            self.game_objects.remove(to_remove)
            del to_remove

        if self.key_handler[key.ENTER]:
            camera.zoom_in()

        if self.key_handler[key.TAB]:
            camera.zoom_out()

        if self.key_handler[key.D]:
            camera.pan(10, 0)

        if self.key_handler[key.W]:
            camera.pan(0, 10)

        if self.key_handler[key.A]:
            camera.pan(-10, 0)

        if self.key_handler[key.S]:
            camera.pan(0, -10)



class Terrain(object):

    def __init__(self, x_dimensions = 0, y_dimensions = 0, mountain_seed = 4, hill_seed = 5, swamp_seed = 8, batch = None, *args, **kwargs):

        #Starting the generating at the 0,0 spot
        self.x = 0
        self.y = 0

        #Dimensions - how many squares long and across the map is
        self.x_dimensions = x_dimensions
        self.y_dimensions = y_dimensions

        #Seeds for generators
        self.mountain_seed = mountain_seed
        self.hill_seed = hill_seed
        self.swamp_seed = swamp_seed

        #Batch
        self.batch = batch

        #On startup, launch generate_landscape_grid
        self.terrain_dict = {}
        self.generate_landscape_grid()
        

    def generate_landscape_grid(self):

        x_gen = 0
        y_gen = 0

        for _xnum in range(0,self.x_dimensions):

            for _ynum in range(0,self.y_dimensions):

                terrain_unit_obj = Terrain_Unit(x_coord=x_gen+1, y_coord=y_gen+1, type='Grass', batch=self.batch)
                y_gen += 1

                game_obj.game_objects.append(terrain_unit_obj)
                self.terrain_dict[(terrain_unit_obj.x_coord,terrain_unit_obj.y_coord)] = terrain_unit_obj

                if y_gen >= self.y_dimensions:
                    y_gen = 0


            x_gen += 1

    
    def mountain_generator(self):

        #Seeds the map with starting points for mountains
        for _num in range(0,self.mountain_seed):


            rand_loc_x = random.randint(1,self.x_dimensions)
            rand_loc_y = random.randint(1,self.y_dimensions)

            self.replace_with_mountain(rand_loc_x,rand_loc_y)

        
        #Algorithm for building upon mountains
        #Go through the list of mountain tiles. For each cell adjacent to each tile, give a probability that that tile will become a mountain given how many 
        #tiles adjacent are mountains. Each time the algorithm checks the original mountain tile, it is removed from the list. New mountain tiles are added to the list.

        
        mountain_list = [obj for obj in self.terrain_dict if self.terrain_dict[obj].terrain_type == 'Mountain']

        #while len(mountain_list) != 0:

        for mountain in mountain_list:
            
            neighbor_list = self.find_neighbors(mountain) #squares surrounding mountain tile

            try:

                for neighbor in [obj for obj in neighbor_list if self.terrain_dict[obj].terrain_type != 'Mountain']:

                        try:

                            neighbor_of_neighbor = self.find_neighbors(neighbor)

                            mountain_neighbors = [obj for obj in neighbor_of_neighbor if self.terrain_dict[obj].terrain_type == 'Mountain'] #how many neighbors of neighbors are mountains?

                            neighbor_count = len(mountain_neighbors)

                            chance = random.random()

                            if (neighbor_count == 1 and chance < .9) or (2 <= neighbor_count <= 4 and chance < .4) or (5 <= neighbor_count <= 6 and chance < .3) \
                                or neighbor_count >= 7:

                                self.replace_with_mountain(neighbor[0],neighbor[1])
                                mountain_list.append(neighbor)

                        except KeyError:
                            pass
            except:
                pass

            mountain_list.remove(mountain)


    def hill_generator(self, hill_next_mountain = 2):

        #The first part of this will make every mountain surrounded by two squares of hills to begin with. It also seeds a few random spots with hills for added hillyness

        
        for mountain in [obj for obj in self.terrain_dict if self.terrain_dict[obj].terrain_type == 'Mountain']:
            
            try:

                mountain_neighbors = self.find_neighbors(mountain)

                self.transform_neighbors(mountain_neighbors,'Hill')
            except:
                pass

        for hill in [obj for obj in self.terrain_dict if self.terrain_dict[obj].terrain_type == 'Hill']:
            try:

                hill_neighbors = self.find_neighbors(hill)

                self.transform_neighbors(hill_neighbors,'Hill')
            except:
                pass

         #Seeds the map with starting points for mountains
        
        
        for _num in range(0, self.hill_seed):


            rand_loc_x = random.randint(1,self.x_dimensions)
            rand_loc_y = random.randint(1,self.y_dimensions)

            if self.terrain_dict[rand_loc_x,rand_loc_y].terrain_type == 'Grass':
                self.replace_with_hill(rand_loc_x,rand_loc_y)
            else:
                continue

        #Second part does something similar to hill generator. First it finds the edge of grass that touches hills. Then, it finds how many neighbors are hills
        #and determines whether that grass cell should be a hill. If a new hill is added, it detects the new edge of grass, makes sure it isn't adding it
        #multiple times, and then adds it to the list of grass edges

        grass_edge = self.edge_detector('Grass','Hill')

        already_added = []

        for obj in grass_edge:
            
            try: 
                neighbors = self.find_neighbors(obj)

                hill_count = len([cell for cell in neighbors if self.terrain_dict[cell].terrain_type == 'Hill'])

                chance = random.random()

                if (hill_count == 1 and chance > .7) or (2 <= hill_count <= 6 and chance > .6) or (hill_count >= 7):
                    self.replace_with_hill(obj[0],obj[1])

                    new_edge = self.find_neighbors(obj)
                    
                    for new_item in new_edge:
                        if new_item not in already_added and self.terrain_dict[new_item].terrain_type == 'Grass':
                            grass_edge.append(new_item)
                            already_added.append(new_item)
                        else:
                            pass
                    
                    
            except:
                pass


    def swamp_generator(self):

        for _num in range(0, self.swamp_seed):


            rand_loc_x = random.randint(1,self.x_dimensions)
            rand_loc_y = random.randint(1,self.y_dimensions)

            if self.terrain_dict[rand_loc_x,rand_loc_y].terrain_type == 'Grass':
                self.replace_with_swamp(rand_loc_x,rand_loc_y)
            else:
                continue

        swamp_edge = self.edge_detector('Grass','Swamp')

        already_added = []

        for obj in swamp_edge:
            
            try: 
                neighbors = self.find_neighbors(obj)

                swamp_count = len([cell for cell in neighbors if self.terrain_dict[cell].terrain_type == 'Swamp'])

                chance = random.random()

                if (swamp_count == 1 and chance > .7) or (2 <= swamp_count <= 6 and chance > .5) or (swamp_count >= 7):
                    self.replace_with_swamp(obj[0],obj[1])

                    new_edge = self.find_neighbors(obj)
                    
                    for new_item in new_edge:
                        if new_item not in already_added and self.terrain_dict[new_item].terrain_type == 'Grass':
                            swamp_edge.append(new_item)
                            already_added.append(new_item)
                        else:
                            pass
                    
                    
            except:
                pass
        


    def transform_neighbors(self,neighbors,terrain_input):

        for cell in [obj for obj in neighbors if self.terrain_dict[obj].terrain_type == 'Grass']:

            if terrain_input == 'Hill':
                self.replace_with_hill(cell[0],cell[1])
            
            elif terrain_input == 'Mountain':
                self.replace_with_mountain(cell[0],cell[1])

        
    def find_neighbors(self,tuple):

        x = tuple[0]
        y = tuple[1]

        neighbor_list = [(x+1,y),(x-1,y),(x,y+1),(x,y-1),(x+1,y+1),(x-1,y-1),(x+1,y-1),(x-1,y+1)]

        return neighbor_list

 
    def replace_with_mountain(self,x_coordinate, y_coordinate):

        #First part finds and removes the square that will become the mountain


        dead_obj = self.terrain_dict[(x_coordinate,y_coordinate)]

        new_x = dead_obj.x
        new_y = dead_obj.y

        dead_obj.dead = True

        del self.terrain_dict[(x_coordinate,y_coordinate)]

        #Second part creates a new mountain terrain square in the first part

        new_terrain = Terrain_Unit(x_coord=x_coordinate, y_coord=y_coordinate, terrain_mov_mod=0, terrain_type='Mountain', batch=Resources.terrain_batch)

        new_terrain.x = new_x
        new_terrain.y = new_y

        game_obj.game_objects.append(new_terrain)

        self.terrain_dict[(x_coordinate,y_coordinate)] = new_terrain


    def replace_with_hill(self,x_coordinate,y_coordinate):

        #First part finds and removes the square that will become the hill


        dead_obj = self.terrain_dict[(x_coordinate,y_coordinate)]

        new_x = dead_obj.x
        new_y = dead_obj.y

        dead_obj.dead = True

        del self.terrain_dict[(x_coordinate,y_coordinate)]

        #Second part creates a new hill terrain square in the first part

        new_terrain = Terrain_Unit(x_coord=x_coordinate, y_coord=y_coordinate, terrain_mov_mod=.5, terrain_type='Hill', batch=Resources.terrain_batch)

        new_terrain.x = new_x
        new_terrain.y = new_y

        game_obj.game_objects.append(new_terrain)

        self.terrain_dict[(x_coordinate,y_coordinate)] = new_terrain


    def replace_with_swamp(self,x_coordinate,y_coordinate):

        #First part finds and removes the square that will become the swamp


        dead_obj = self.terrain_dict[(x_coordinate,y_coordinate)]

        new_x = dead_obj.x
        new_y = dead_obj.y

        dead_obj.dead = True

        del self.terrain_dict[(x_coordinate,y_coordinate)]

        #Second part creates a new swamp terrain square in the first part

        new_terrain = Terrain_Unit(x_coord=x_coordinate, y_coord=y_coordinate, terrain_mov_mod=.3, terrain_type='Swamp', batch=Resources.terrain_batch)

        new_terrain.x = new_x
        new_terrain.y = new_y

        game_obj.game_objects.append(new_terrain)

        self.terrain_dict[(x_coordinate,y_coordinate)] = new_terrain


    def edge_detector(self,edge,boundary):

        list_of_edges = []

        #Search through every instance of the boundary and see which cells are the edge

        for cell in [obj for obj in self.terrain_dict if self.terrain_dict[obj].terrain_type == boundary]:
            try:
                neighbors = self.find_neighbors(cell)

                for obj in neighbors:
                    if self.terrain_dict[obj].terrain_type == edge:
                        list_of_edges.append(obj)
            except:
                pass

        return list_of_edges





class Terrain_Unit(object):

    def __init__(self, x_coord = 0, y_coord = 0, unit_size = 10, terrain_mov_mod = 1, terrain_type='Grass', batch = None, *args, **kwargs):

        super().__init__()

        #Unit size is how many pixels each square is
        self.unit_size = unit_size

        #Batch
        self.batch = batch

        self.dead = False

        #Initiatlizes grid coordinates for the map
        self.x_coord = x_coord
        self.y_coord = y_coord

        #Establishes location in pixel space
        self.x = self.x_coord * self.unit_size
        self.y = self.y_coord * self.unit_size

        #How difficult is it to move through this terrain
        self.terrain_mov_mod = terrain_mov_mod

        #Set sprite
        self.terrain_type = terrain_type
 
        self.terrain_sprite = self.set_terrain()


        #print('Terrain unit initialized')
        #print(self.unit_size)
        #print(self.x_coord, self.y_coord)

    def update(self,dt, camera):
        camera.update_sprite(self.terrain_sprite, self.x, self.y)

    def set_terrain(self):
        
        #Initializes with grass image
        if self.terrain_type == 'Grass':
            sprite_img = Resources.grass_img
            sprite_img.height = self.unit_size
            sprite_img.width = self.unit_size
            grass_sprite = pyglet.sprite.Sprite(sprite_img, x = self.x, y = self.y, batch = self.batch)
            return grass_sprite

        #Initializes with mountain image
        elif self.terrain_type == 'Mountain':
            sprite_img = Resources.mountain_img
            sprite_img.height = self.unit_size
            sprite_img.width = self.unit_size
            mountain_sprite = pyglet.sprite.Sprite(sprite_img, x = self.x, y = self.y, batch = self.batch)
            return mountain_sprite

        #Initializes with hill image
        elif self.terrain_type == 'Hill':
            sprite_img = Resources.hill_img
            sprite_img.height = self.unit_size
            sprite_img.width = self.unit_size
            hill_sprite = pyglet.sprite.Sprite(sprite_img, x = self.x, y = self.y, batch = self.batch)
            return hill_sprite

        #Initializes with swamp image
        elif self.terrain_type == 'Swamp':
            sprite_img = Resources.swamp_img
            sprite_img.height = self.unit_size
            sprite_img.width = self.unit_size
            swamp_sprite = pyglet.sprite.Sprite(sprite_img, x = self.x, y = self.y, batch = self.batch)  
            return swamp_sprite




#Initiating Objects

Test_Player = Player(batch=Resources.player_batch)



game_obj = GamePlay(x=0,y=0)

game_obj.game_objects.extend([Test_Player])

terrain_obj = Terrain(x_dimensions=100, y_dimensions = 80, unit_size=20, batch=Resources.terrain_batch)
