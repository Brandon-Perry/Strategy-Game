import pyglet
import Resources
import Functions
import Terrain
import Objects


import math
from pyglet.window import key
from pyglet.window import mouse
import random




class Agents(object):
    '''Superclass of Player and Enemy'''
    def __init__(self, x=0.0, y=0.0, *args,**kwargs):

        self.sprite = pyglet.sprite.Sprite(*args, **kwargs)

        #Location of object in world
        self.x = x
        self.y = y

        #self.current_cell = Terrain.terrain_obj.return_cell_index(self.x,self.y)

        #Physics
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.speed = 0
        self.mass = 0
        self.rotate_speed = 0
        self.rotation = 0

        #Alive status
        self.dead = False

        #Handles navigation
        self.navigation = False
        self.nav_path = []
        self.nav_index = 0
        self.available_nav_coords = []
        self.distance_to_nav_coords = {}


        #Action point restrictions
        self.move_points = 5

        #Firing
        self.targeting = False
        self.target = None


    def update(self,dt, camera):


        #Handles navigation
        if self.navigation == True:
            self.navigate_path(self.nav_path[self.nav_index],dt)

        self.x,self.y = Terrain.terrain_obj.return_cell_position(self.current_cell)

        #Velocity and how it affects movement (dt is frame)
        #self.x += self.velocity_x * dt
        #self.y += self.velocity_y * dt
        camera.update_sprite(self.sprite, self.x, self.y)

        #Handles firing
        if self.targeting == True:
            self.fire_weapon(self.target)


    def navigate_path(self,point,dt):
        '''Accepts global coordinate. Rotates to point and moves forward until it's at its destination. Uses self.nav_coords to follow multi-point path'''
        ####First rotate to the correct position

        #Find angle between current position and point

        #angle changed to negative because the way pyglet sets object orientation

        angle_to_point = -math.degrees(Functions.angle(point_1=(self.x,self.y),point_2=point))

        if math.fmod(self.rotation, 360) > angle_to_point:
            if math.fmod(self.rotation,360) - angle_to_point < self.rotate_speed:
                self.rotation = angle_to_point
            else:
                self.rotation -= self.rotate_speed

        if math.fmod(self.rotation, 360) < angle_to_point:
            if angle_to_point - math.fmod(self.rotation,360) < self.rotate_speed:
                self.rotation = angle_to_point
            else:
                self.rotation += self.rotate_speed

        #If player is at the correct angle, then go forward. If the point is within the vector-space, stop at the point instead.
        if math.fmod(self.rotation,360) == angle_to_point and (int(self.x),int(self.y)) != point:
            #angle_radians = -math.radians(self.rotation)

            #vector_x = math.cos(angle_radians) * self.speed * dt
            #vector_y = math.sin(angle_radians) * self.speed * dt

            #print('vectorx',vector_x)
            #print('vectory',vector_y)

            self.current_cell = Terrain.terrain_obj.return_cell_index(point[0],point[1])
            print(self.current_cell)
            '''
            if ((vector_x >= 0 and self.x + vector_x >= (goal_cell.x - goal_cell.size/2)) or (vector_x <= 0 and self.x - vector_x <= (goal_cell.x + goal_cell.size/2))) and \
                ((vector_y >= 0 and self.y + vector_y >= (goal_cell.y - goal_cell.size/2)) or (vector_y <= 0 and self.y - vector_y <= (goal_cell.y + goal_cell.size/2))):
                self.x = point[0]
                self.y = point[1]
                #print('latched')

            else:

                self.x += vector_x
                self.y += vector_y
                #self.x = int(round(self.x))
                #self.y = int(round(self.y))
                #print('point',point)
                #print('position',self.x,self.y)

            '''
        #If the player is at the point, then either adjust the point to the next in list or stop navigation if at end
        if (int(self.x),int(self.y)) == point:

            if point == self.nav_path[-1]:
                self.nav_index = 0
                self.navigation = False

                print('here!')

            else:
                self.nav_index += 1







        #print('sprite position',self.sprite.position)
        #print('target position',point)
        #print('`````````')


    def return_sprite_cell(self):
        '''Returns whichever tile coordinate the Agent sprite is touching'''

        for coord in Terrain.terrain_obj.terrain_dict:

            cell = Terrain.terrain_obj.terrain_dict[coord]

            if cell.sprite.x - cell.sprite.width/2 < self.sprite.x < cell.sprite.x + cell.sprite.width/2 and \
                    cell.sprite.y - cell.sprite.height/2 < self.sprite.y < cell.sprite.y + cell.sprite.height/2:

                    return coord


    def subtract_movement_score(self,path_list):
        '''Takes the path_list of the object and substracts the distance from the movement score'''
        sum_distance = 0

        for unit in path_list:

            if unit == path_list[0]:
                continue

            previous_index = path_list.index(unit) - 1

            sum_distance += (Functions.distance(point_1=(unit),point_2=(path_list[previous_index])) * Terrain.terrain_obj.terrain_dict[unit].terrain_mov_mod)

        self.move_points -= sum_distance


    def fire_weapon(self,target):
        '''Takes target, rotates to face target, and then if rotation complete, fires at target. Runs via update if targeting is True'''
        #First, aim at target
        angle_to_point = -math.degrees(Functions.angle(point_1=(self.x,self.y),point_2=(target.x,target.y)))

        if math.fmod(self.rotation, 360) > angle_to_point:

            if math.fmod(self.rotation,360) - angle_to_point < self.rotate_speed:
                self.rotation = angle_to_point
            else:
                self.rotation -= self.rotate_speed

        if math.fmod(self.rotation, 360) < angle_to_point:
            if angle_to_point - math.fmod(self.rotation,360) < self.rotate_speed:
                self.rotation = angle_to_point
            else:
                self.rotation += self.rotate_speed

        #If player is at the correct angle, then go forward. If the point is within the vector-space, stop at the point instead.
        if math.fmod(self.rotation,360) == angle_to_point:
            self.targeting = False
            print('Targeting complete')

            new_laser = Laser(x=self.x, y=self.y, rotation=angle_to_point, target=self.target, batch=Resources.effects_batch)
            Objects.game_obj.game_objects.append(new_laser)


    def return_if_x_y_in_sprite_loc(self,x,y):
        if (self.sprite.x - self.sprite.width//2 <= x <= self.sprite.x + self.sprite.width//2) and \
            (self.sprite.y - self.sprite.height//2 <= y <= self.sprite.y + self.sprite.width//2):
            return True
        else:
            return False


    def attack_target(self,target):
        '''Sets the Agent.target to the target and turns targeting on, which activates the fire_weapon method during update'''
        self.targeting = True
        self.target = target


    def handle_navigation(self,x,y):
        '''Handles all navigation code for the agent. Use global coordinates. If the tile is too far or impassible, won't move.'''
        player_cell = Terrain.terrain_obj.return_player_cell(self)
        destination_cell = Terrain.terrain_obj.return_sprite_index(x,y)
        #print('left click, player cell',player_cell)
        #print('left click, destination cell',destination_cell)
        print(x,y)

        if Terrain.terrain_obj.terrain_dict[destination_cell].terrain_mov_mod == math.inf:
            print('Cant navigate to this cell')
        elif destination_cell not in Terrain.terrain_obj.highlighted_terrain:
            print('Cell is too far away or not navigatable')
        else:

            nav_list = Terrain.terrain_obj.Dijkstra_algorithm(player_cell,destination_cell)

            nav_path = Terrain.terrain_obj.return_list_cell_positions(nav_list)

            self.nav_path = nav_path
            self.navigation = True

            self.subtract_movement_score(nav_list)
            #print(player.move_points)

class Laser(object):

    def __init__(self, x, y, rotation, target, *args,**kwargs):

        self.x = x
        self.y = y

        self.rotation = rotation

        self.target = target

        self.speed = 10000

        self.dead = False

        self.sprite = pyglet.sprite.Sprite(img=Resources.laser_img,*args, **kwargs)

    def update(self,dt, camera):

        if self.dead == True:
            return


        super().__init__()

        self.sprite.rotation = self.rotation

        angle_radians = -math.radians(self.rotation)

        velocity_x = math.cos(angle_radians) * self.speed * dt
        velocity_y = math.sin(angle_radians) * self.speed * dt

        self.x += velocity_x * dt
        self.y += velocity_y * dt
        camera.update_sprite(self.sprite, self.x, self.y)

        self.check_collision()


    def return_if_x_y_in_sprite_loc(self,x,y):
        '''Checks to see if sprites overlap with other x,y position'''
        if (self.sprite.x - self.sprite.width//2 <= x <= self.sprite.x + self.sprite.width//2) and \
            (self.sprite.y - self.sprite.height//2 <= y <= self.sprite.y + self.sprite.width//2):
            return True
        else:
            return False

    def check_collision(self):
        '''If laser comes into contact with mountain tile, dead laser. If contact with target, kill laser and target'''
        if self.target.return_if_x_y_in_sprite_loc(self.sprite.x,self.sprite.y):
            Objects.game_obj.remove_dead(self.target)
            Objects.game_obj.remove_dead(self)

        for coord in [obj for obj in Terrain.terrain_obj.terrain_dict if \
            Terrain.terrain_obj.terrain_dict[obj].terrain_mov_mod == math.inf]:
            
            check_cell = Terrain.terrain_obj.terrain_dict[coord]
            if self.return_if_x_y_in_sprite_loc(check_cell.sprite.x,check_cell.sprite.y):
                print(coord,check_cell.sprite.x,check_cell.sprite.y,check_cell.sprite.height)

                print(self.sprite.position,self.sprite.height,self.sprite.width)

                Objects.game_obj.remove_dead(self)
                return

