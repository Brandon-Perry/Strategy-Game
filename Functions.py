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