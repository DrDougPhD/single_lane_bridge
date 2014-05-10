#Vehicle.py
#
#Written by Madeline Cameron and Doug McGeehan
#CS 384 - Distributed Operating Systems
#Spring 2014

import random
import cocos
import time
import math
import threading
from cocos.actions import MoveTo
from cocos.actions import RotateTo
from UI import RoadPoints


class Car_Status(): #You can totally tell I am a C# developer... can't you?
    Moving = 0      # That's how I would have done it :P
    Waiting = 1
    Warning = 2
    On_Bridge = 3

class Vehicle:
    def __init__(self, index, speed, direction):
        print("Initializing vehicle {0}...".format(index))

        #"Bridge" is road 3 and no one can start there
        random_road = random.choice([0, 1, 2, 4, 5, 6]) 

        self.current_road = random_road
        self.timestamp = -1
        self.index = index
        self.speed = speed
        self.direction = direction
        self.status = Car_Status.Moving
        self.road_completed_percentage = 0
        self.road_map = RoadPoints.ROADMAP
        self.label = None

        self.sprite = cocos.sprite.Sprite(
          'car2.png',
          scale=0.10,
          color=[random.randrange(0, 255) for i in range(3)]
        ) #Pick a random color
        self.sprite.position = self.road_map[self.current_road][0]

        self.rotate_vehicle()
        print("Vehicle {0} initialized!".format(index))


    def rotate_vehicle(self):
        if self.current_road % 2 == 0: #Vehicle rotation
            mod = 0
            if self.current_road == 0 or self.current_road == 4:
                if self.current_road == 4:
                    mod = -1
                else:
                    mod = -4.2142857
            else:
                if self.current_road == 2:
                    mod = 1
                else:
                    mod = 4.2142857
            self.sprite.do(RotateTo(mod*56, 0))
        if self.current_road == 1 or self.current_road == 5:
            mod = 0
            if self.current_road == 1:
                mod = -1
            else:
                mod = 1
            self.sprite.do(RotateTo(mod*90, 0))
        if self.current_road == 3:
            self.sprite.do(RotateTo(0, 0))


    def create_timestamp(self):
        self.timestamp = time.time()

    def move(self):
        # If the road has been traveled and not on road 2 or 6
        if self.road_completed_percentage >= 1 and self.status != Car_Status.Warning:
            self.current_road += 1 # Go to the next road
            self.road_completed_percentage = 0 # Start over
            self.rotate_vehicle()

        else:
            # Stop short before bridge, mostly cosmetic
            if self.road_completed_percentage >= 0.85 and self.status == Car_Status.Warning:
                self.status = Car_Status.Waiting
                self.create_timestamp()
                return
            if self.status == Car_Status.On_Bridge:
                self.road_completed_percentage = 0
                self.current_road = 3
                self.sprite.do(RotateTo(0, 0))

        start, end = self.road_map[self.current_road]
        start_x, start_y = start
        end_x, end_y = end
        road_length = math.hypot(end_x - start_x, end_y - start_y)

        self.road_completed_percentage += (1.0 / road_length) * (1 + self.speed / 100) #Step size
        move_to = (
          (start_x + ((end_x - start_x) * self.road_completed_percentage)),
          (start_y + ((end_y - start_y) * self.road_completed_percentage))
        )
        self.sprite.do(MoveTo(move_to, 0.6))

        self.label.position = (
          move_to[0] + 10,
          move_to[1] + 10
        )
        #label_move_to = sprite_move_to[0], sprite_move_to[0]+10
        #self.label.do(MoveTo(label_move_to, 0.6))


    def check_for_bridge(self):
        if self.status == Car_Status.Waiting:
            print("Vehicle {0} is waiting at the bridge!".format(self.index))
            #return self.handle_cs()

        car_is_approaching_bridge = (
          (self.current_road == 2) or
          (self.current_road == 6)
        )
        if car_is_approaching_bridge and self.status == Car_Status.Moving:
            print("Vehicle {0} is near the bridge!".format(self.index))
            self.status = Car_Status.Warning
            return True
