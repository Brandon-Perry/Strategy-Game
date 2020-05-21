import pyglet
import Resources
import math
from pyglet.window import key
from pyglet.window import mouse
import Functions
import random

global_key_handler = key.KeyStateHandler()
global_mouse_handler = mouse.MouseStateHandler()
global_mouse_coordinates = 0,0

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
        min_x = self.sprite.width / 2
        min_y = self.sprite.height / 2
        max_x = 800 - self.sprite.width / 2
        max_y = 600 - self.sprite.height / 2
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
        collision_distance = self.sprite.width/2 + other_object.width/2
        actual_distance = Functions.distance(self.sprite.position,other_object.position)
        return (actual_distance <= collision_distance)
    
    def handle_collision_with(self,other_object): 
        
        pass

        
  
class Player(PhyiscalObject):

    def __init__(self,x=400,y=100.0,*args,**kwargs):
        super().__init__(img=Resources.spider_tank,*args,**kwargs)

        self.x = x
        self.y = y

        #self.sprite = pyglet.sprite.Sprite(img= Resources.spider_tank)

        #Ship physics
        self.speed = 300.0
        self.mass = 1.0
        self.rotate_speed = 25
        self.rotation = 0
        
        #Ship handling
        self.key_handler = global_key_handler
        self.mouse_handler = global_mouse_handler
        self.traveling = False
        self.travel_to = None

        #Player's attributes
        self.lives = 3

    def update(self,dt, camera):

        super(Player,self).update(dt, camera)
        self.thrusters(dt)
        self.sprite.rotation = self.rotation

        self.path_finding(dt)



    def thrusters(self,dt):
        #Rotation
        if self.key_handler[key.LEFT]:
            self.rotation -= self.rotate_speed * dt

        if self.key_handler[key.RIGHT]:
            self.rotation += self.rotate_speed * dt

        #Thrust and deceleration
        if self.key_handler[key.UP]:
            angle_radians = -math.radians(self.rotation)
            self.velocity_x = math.cos(angle_radians) * self.speed * dt
            self.velocity_y = math.sin(angle_radians) * self.speed * dt
    

        if not self.key_handler[key.UP]:
            self.velocity_x = 0
            self.velocity_y = 0
        
    
    def path_finding(self,dt):

        if self.mouse_handler[mouse.LEFT]:
            
            self.traveling = True

            


            path = self.dijkstra_search(self.player_cell_location(), self.click_cell_location(global_mouse_coordinates))
            self.draw_path(path)

        #self.travel_to_location(self.travel_to,dt)

    
    def player_cell_location(self):

        player_position = self.x,self.y

        for coord in terrain_obj.terrain_dict:

            cell = terrain_obj.terrain_dict[coord]
            #print(cell)

            if (cell.x - (cell.unit_size/2) <= player_position[0] <= cell.x + (cell.unit_size/2)) \
                and (cell.y - (cell.unit_size/2) <= player_position[1] <= cell.y + (cell.unit_size/2)):

                print('player posx',player_position[0])
                print('player posy', player_position[1])
                print('cellx',cell.x)
                print('celly,',cell.y)
                print('coord',coord)

                return coord


    def click_cell_location(self,global_mouse_coordinates):

        mouse_position = global_mouse_coordinates

        for coord in terrain_obj.terrain_dict:

            cell = terrain_obj.terrain_dict[coord]

            if (cell.sprite.x - cell.sprite.width/2 <= mouse_position[0] <= cell.sprite.x + cell.sprite.width/2) \
                and (cell.sprite.y - cell.sprite.height/2 <= mouse_position[1] <= cell.sprite.y + cell.sprite.height/2):

                print('clickx',mouse_position[0])
                print('clicky',mouse_position[1])
                print('cellx',cell.x)
                print('celly',cell.y)
                print('coord',coord)

                return coord



    def dijkstra_search(self, start_node, end_node):

        #List of cells that have already ran through the algorithm, don't need to go back to
        already_searched = []

        #List of nodes and their (total) shortest path values
        node_distance = {}

        #List of nodes and the nodes that are the shortest path to them
        previous_node = {}

        #Priority Que
        priority_que = []

        #Sets the value of nodes to an arbitrarily large number to start with
        for node in terrain_obj.terrain_dict:
            node_distance[node] = 10^100000

        #Changes the value of the start node to be zero.
        node_distance.update({start_node:0})


        #The node currently being examined. Starts at start_node
        current_node = start_node


        


        dijkstra_search = True
    

        while dijkstra_search == True:
            
            #Search the neighbors of the current node
            neighbors = Functions.find_neighbors(current_node)

            
            for cell in [obj for obj in neighbors if obj not in already_searched]:
                
                try:
                    #Find the distance from the current node to the neighbor node


                    cell_obj = terrain_obj.terrain_dict[cell]
                    current_node_obj = terrain_obj.terrain_dict[current_node]

                    #Create exception for mountain tiles
                    if cell_obj.terrain_type == "Mountain":
                        continue

                    distance = Functions.distance((cell_obj.x,cell_obj.y),(current_node_obj.x,current_node_obj.y)) / current_node_obj.terrain_mov_mod

                    #If the total distance (distance to neighbor node and the neighbor node's to the beginning) is smaller that what's already
                    #Listed, then update the distance and path dictionary
                    total_distance = distance + node_distance[current_node]
                    #print(total_distance)
                    #print(node_distance[cell])
                    #print(cell)

                    if total_distance < node_distance[cell]:
                        node_distance.update({cell:total_distance})
                        #print('node distance',node_distance[cell])
                        previous_node.update({cell:current_node})
                        #print('previous node',previous_node[cell])
                        priority_que.append(cell)
                        #print(priority_que)
                except KeyError:
                    pass

            #Adds the current cell to the list of already searched spaces
            already_searched.append(current_node)
            if current_node in priority_que:
                priority_que.remove(current_node)
            #print(already_searched)

            #Finds the lowest value in the priority que and sets it to the current node
            current_node = priority_que[0]
            for coord in [obj for obj in priority_que if terrain_obj.terrain_dict[obj].terrain_type != 'Mountain']:
                if node_distance[coord] < node_distance[current_node]:
                    current_node = coord

            #print(current_node)
            
            if end_node in already_searched:
                try:
                    path_result = [end_node]
                    step_in_path = end_node
                    path_search = True
                    while path_search == True:
                        x = previous_node[step_in_path]
                        path_result.append(x)
                        step_in_path = x
                        
                        if step_in_path == start_node:
                            #path_result.append(start_node)
                            print(path_result)
                            print('player sprite loc',self.sprite.position)
                            return path_result
                except:
                    pass

    def draw_path(self,path_list):

        for cell in path_list:

            tile = terrain_obj.terrain_dict[cell]

            tile.sprite = Resources.black_img
    



    def travel_to_location(self,location,dt):
        
        
        if self.traveling == True:
            if round(-math.radians(self.rotation),2) < round(Functions.angle(self.sprite.position,location),2):
                
        
                self.rotation -= self.rotate_speed * dt

                print('less than')
                print(Functions.angle(self.sprite.position, location))
                print(math.radians(self.rotation))


            elif round(-math.radians(self.rotation),2) > round(Functions.angle(self.sprite.position,location),2):

                              
                self.rotation += self.rotate_speed * dt


                print('greater than')
                print(Functions.angle(self.sprite.position, location))
                print(math.radians(self.rotation))
            
            
            else:
                

                angle_radians = -math.radians(self.rotation)
                self.velocity_x = math.cos(angle_radians) * self.speed * dt
                self.velocity_y = math.sin(angle_radians) * self.speed * dt

                #if ((self.position[0] - self.width/2),(self.position[1] - self.height/2)) <= location <= ((self.position[0] + self.width/2),(self.position[1] + self.height/2)):
                    #self.traveling = False

                pos_x = self.sprite.position[0]
                pos_y = self.sprite.position[1]

                if (round(pos_x), round(pos_y)) == (round(location[0]),round(location[1])):
                    self.traveling = False


    


    

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

        #Handles Camera zooming and panning
        if self.key_handler[key.ENTER]:
            camera.zoom_in()

        if self.key_handler[key.TAB]:
            camera.zoom_out()

        if self.key_handler[key.W]:
            camera.pan(0,10)

        if self.key_handler[key.A]:
            camera.pan(-10,0)
        
        if self.key_handler[key.D]:
            camera.pan(10,0)

        if self.key_handler[key.S]:
            camera.pan(0,-10)

        
        

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
            
            neighbor_list = Functions.find_neighbors(mountain) #squares surrounding mountain tile

            try:

                for neighbor in [obj for obj in neighbor_list if self.terrain_dict[obj].terrain_type != 'Mountain']:

                        try:

                            neighbor_of_neighbor = Functions.find_neighbors(neighbor)

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

                mountain_neighbors = Functions.find_neighbors(mountain)

                self.transform_neighbors(mountain_neighbors,'Hill')
            except:
                pass

        for hill in [obj for obj in self.terrain_dict if self.terrain_dict[obj].terrain_type == 'Hill']:
            try:

                hill_neighbors = Functions.find_neighbors(hill)

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
                neighbors = Functions.find_neighbors(obj)

                hill_count = len([cell for cell in neighbors if self.terrain_dict[cell].terrain_type == 'Hill'])

                chance = random.random()

                if (hill_count == 1 and chance > .7) or (2 <= hill_count <= 6 and chance > .6) or (hill_count >= 7):
                    self.replace_with_hill(obj[0],obj[1])

                    new_edge = Functions.find_neighbors(obj)
                    
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
                neighbors = Functions.find_neighbors(obj)

                swamp_count = len([cell for cell in neighbors if self.terrain_dict[cell].terrain_type == 'Swamp'])

                chance = random.random()

                if (swamp_count == 1 and chance > .7) or (2 <= swamp_count <= 6 and chance > .5) or (swamp_count >= 7):
                    self.replace_with_swamp(obj[0],obj[1])

                    new_edge = Functions.find_neighbors(obj)
                    
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
                neighbors = Functions.find_neighbors(cell)

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
 
        self.sprite = self.set_terrain()


        #print('Terrain unit initialized')
        #print(self.unit_size)
        #print(self.x_coord, self.y_coord)

    def update(self,dt, camera):
        camera.update_sprite(self.sprite, self.x, self.y)

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

        elif self.terrain_type == 'Black':
            sprite_img = Resources.black_img
            sprite_img.height = self.unit_size
            sprite_img.width = self.unit_size
            black_sprite = pyglet.sprite.Sprite(sprite_img, x = self.x, y = self.y, batch = self.batch)
            return black_sprite




#Initiating Objects

Test_Player = Player(batch=Resources.player_batch)



game_obj = GamePlay(x=0,y=0)

game_obj.game_objects.extend([Test_Player])

terrain_obj = Terrain(x_dimensions=100, y_dimensions = 100, unit_size=10, batch=Resources.terrain_batch)
