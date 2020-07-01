import pyglet
import math
import random


def distance(point_1=(0,0), point_2=(0,0)):
    #returns the distance between two points

    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)


def angle(point_1=(0,0), point_2=(0,0)):
    return math.atan2(point_2[1] - point_1[1],point_2[0] - point_1[0])


def collision_check(game_objects):
    #Checks each object active to see if collision kills
    for i in range(len(game_objects)):
        for j in range(i+1, len(game_objects)):
            obj_1 = game_objects[i]
            obj_2 = game_objects[j]

        if obj_1.collides_with(obj_2):
            obj_1.handle_collision_with(obj_2)
            obj_2.handle_collision_with(obj_1)

def find_neighbors(tuple):

    x = tuple[0]
    y = tuple[1]

    neighbor_list = [(x+1,y),(x-1,y),(x,y+1),(x,y-1),(x+1,y+1),(x-1,y-1),(x+1,y-1),(x-1,y+1)]

    return neighbor_list

def path_straightner(path):

    #Looks through list and finds angle of direction at each point. If it's the same as before, then remove that previous one.

    new_path = []

    for coord in path:

        if coord == path[0] or coord == path[1]:
            new_path.append(coord)

        else:

            angle_between_points = angle(point_1=new_path[-1],point_2=coord)

            angle_previous_points = angle(point_1=new_path[-2],point_2=new_path[-1])

            if angle_between_points == angle_previous_points:

                new_path.pop(-1)


            new_path.append(coord)

            if coord == path[-1]:
                return new_path



