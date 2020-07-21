#Import modules
import pyglet
import math
import random
from pyglet.window import mouse
from pyglet.window import key

#Game files
import Objects
import Players
import Terrain
import Resources
import Functions
import math
import Agents


class Enemy(Agents.Agents):
    '''Enemy object that plays against the player. Superclass = Agents'''
    def __init__(self, x=0, y=0, name=None, *args, **kwargs):

        self.x = x
        self.y = y

        super().__init__(img=Resources.alien_tank,*args,**kwargs)

        self.x = x
        self.y = y
        self.name = name

        self.sprite = pyglet.sprite.Sprite(img= Resources.alien_tank, batch = Resources.enemy_batch)
        self.sprite.scale = .1

        #Enemy handling
        self.key_handler = Objects.global_key_handler
        self.mouse_handler = Objects.global_mouse_handler

        #Enemy physics
        self.speed = 300.0
        self.mass = 1.0
        self.rotate_speed = 8
        self.rotation = 0

        #Enemy's attributes
        self.lives = 3

        #Handles navigation
        self.navigation = False
        self.nav_path = []
        self.nav_index = 0
        self.shot_prep_status = False

        #Action point restrictions
        self.move_points = 10
        self.max_move_points = 10

        #Enemy selected
        self.selected = False


    def update(self,dt, camera):

        super(Enemy,self).update(dt, camera)
        self.sprite.rotation = self.rotation

        #Handles navigation
        if self.navigation == True:
            self.navigate_path(self.nav_path[self.nav_index],dt)


        #Handles changing turn
        if self.key_handler[key.T]:
            if Objects.game_obj.player_turn == True:
                Objects.game_obj.player_turn = False
                self.handle_enemy_turn()

        #If the enemy is moving to make a shot, then check and see if it has reached its destination and make a shot if so
        if self.shot_prep_status == True:
            if self.navigation == False:
                self.attack_target(self.target)
                self.shot_prep_status = False


    def return_if_have_shot(self,start_node,target):
        '''Uses linear equation to determine if, starting from a particular tile, if it has a clean shot at the target'''
        #First, define the starting and ending positions
        start_cell = Terrain.terrain_obj.terrain_dict[start_node]
        target_coord = Terrain.terrain_obj.return_cell_index(target.x,target.y)
        target_cell = Terrain.terrain_obj.terrain_dict[target_coord]

        #Linear equation parameters
        t = 10
        x = start_cell.x
        y = start_cell.y
        bottom_fact = math.sqrt(((target_cell.x - start_cell.x) * (target_cell.x - start_cell.x)) + \
                ((target_cell.y - start_cell.y) * (target_cell.y - start_cell.y)))
        x_fact = (target_cell.x - start_cell.x) / bottom_fact
        y_fact = (target_cell.y - start_cell.y) / bottom_fact

        #List of cells that pass between two points
        available_coords = []

        #While loop until reached target cell
        test_limit = 1000
        iter = 0
        while True:
            x += t * x_fact
            y += t * y_fact

            new_coord = Terrain.terrain_obj.return_cell_index(x,y)
            #print(x,y)
            #print(new_coord)

            if new_coord not in available_coords:
                available_coords.append(new_coord)

            #If searched has reached its end, then find neighbors and return false if mountains, else true
            if target_coord in available_coords:

                neighbor_list = []
                for coord in available_coords:
                    neighbors = Functions.find_neighbors(coord)
                    for neighbor in neighbors:
                        if neighbor not in neighbor_list and neighbor not in available_coords:
                            neighbor_list.append(neighbor)
                available_coords.extend(neighbor_list)

                for coord in available_coords:
                    if Terrain.terrain_obj.terrain_dict[coord].terrain_mov_mod == math.inf:
                        #print('mountain the way')
                        return False
                
                #Terrain.terrain_obj.color_path(available_coords)
                #print('has a shot')
                return True


            iter += 1
            if iter > test_limit:
                print(available_coords)

                #Terrain.terrain_obj.color_path(available_coords)
                print('got to iter end')
                return False
            

    def check_if_shot_available_surrounding_nodes(self,target):
        '''Takes target, and using return_if_have_shot(self,start_node,target) determines if the object's available nodes have any available shots'''
        
        shot_list = []

        #for coord in available movement cells, see if they are able to take a shot from
        for coord in self.available_nav_coords:

            if self.return_if_have_shot(coord,target):
                shot_list.append(coord)
            else:
                pass
        
        if len(shot_list) == 0:
            print('cant take a shot this round')
            return False
        elif len(shot_list) > 0:
            return shot_list


    def nav_to_closest_shot(self,shot_list):
        '''Takes a list of tile coords, finds the shortest distance (dist func), and navigates to that coord'''

        shortest_distance = self.distance_to_nav_coords[shot_list[0]]
        shortest_node = shot_list[0]

        for node in shot_list:
            if self.distance_to_nav_coords[node] < shortest_distance:
                shortest_distance = self.distance_to_nav_coords[node]
                shortest_node = node
        
        destination_cell = Terrain.terrain_obj.terrain_dict[shortest_node]
        self.handle_navigation(destination_cell.x,destination_cell.y)


    def handle_attacking(self,target):
        '''Takes target object and handles initial attacking sequence. If no available shot immediately, uses nav_to_closest shot to navigate to point /
            turns prep_shot_status on to tell object that at end of navigation, take a shot (located in def update)'''
        #First, see if there's an open shot at current position
        self_node = Terrain.terrain_obj.return_cell_index(self.x,self.y)

        if self.return_if_have_shot(self_node,target):
            self.attack_target(target)
            #end func
            return

        #If not, see if available cells have an open shot
        shot_list = self.check_if_shot_available_surrounding_nodes(target)

        #If not, end func. Else, navigate to closest cell with shot
        if shot_list == False:
            return
        else:

            self.nav_to_closest_shot(shot_list)
            self.shot_prep_status = True
            self.target = target
    
        
    def handle_enemy_turn(self):
        '''Contains all the code for running the enemy object's turn.'''
        #First, select self and return available terrain
        available_coords = Terrain.terrain_obj.move_distance_calc(self)
        #print('available coords',available_coords)
        Terrain.terrain_obj.reset_highlighted_terrain()
        Terrain.terrain_obj.highlight_terrain_func(available_coords)

        #Choose target. Based on distance
        distance_to_player = {}
        for player in [obj for obj in Objects.game_obj.game_objects if obj.__class__ == Players.Player]:
            print(player)
            distance_to_player[player] = Functions.distance((self.x,self.y),(player.x,player.y))

        distance = math.inf
        chosen_player = None
        for player in distance_to_player:
            if distance_to_player[player] < distance:
                chosen_player = player
                distance = distance_to_player[player]
        print(chosen_player)
        #Attack chosen player
        self.handle_attacking(chosen_player)

        #Next turn
        #Objects.game_obj.player_turn = True


#Initializing Object
Enemy1 = Enemy(x=400,y=400,name='Enemy1',batch=Resources.enemy_batch)
