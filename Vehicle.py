#Vehicle.py
#
#Written by Madeline Cameron and Doug McGeehan
#CS 384 - Distributed Operating Systems
#Spring 2014

import random, cocos, time, math, threading
from cocos.actions import MoveTo, RotateTo
from UI import RoadPoints


class Car_Status(): #You can totally tell I am a C# developer... can't you?
    Moving = 0      # That's how I would have done it :P
    Waiting = 1
    Warning = 2
    On_Bridge = 3

class Vehicle():
    def __init__(self, index, speed, direction):
        print("Initializing vehicle " + str(index) + "...")

        random_road = 3
        while random_road == 3: #"Bridge" is road 3 and no one can start there
            random_road = random.randrange(0, 7)

        self.current_road = random_road
        self.timestamp = -1
        self.index = index
        self.speed = speed
        self.direction = direction
        self.status = Car_Status.Moving
        self.position = 0
        self.road_map = RoadPoints.ROADMAP
        self.label = None
        self.sprite = cocos.sprite.Sprite(
          'car2.png',
          scale=0.10,
          color=[random.randrange(0, 255) for i in range(3)]
        ) #Pick a random color
        self.sprite.position = self.road_map[self.current_road][0]

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

        print("Vehicle " + str(index) + " initialized!")

    def create_timestamp(self):
        self.timestamp = time.time()

    def move(self):
        if self.position >= 1 and self.status != Car_Status.Warning: #If the road has been traveled and not on road 2 or 6
            self.current_road += 1 #Go to the next road
            self.position = 0 #Start over

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
        else:
            if self.position >= 0.85 and self.status == Car_Status.Warning: #Stop short before bridge, mostly cosmetic
                self.status = Car_Status.Waiting
                self.create_timestamp()
                return
            if self.status == Car_Status.On_Bridge:
                self.position = 0
                self.current_road = 3
                self.sprite.do(RotateTo(0, 0))

        current_road_start_loc = self.road_map[self.current_road][0]
        current_road_end_loc = self.road_map[self.current_road][1]
        road_length = math.sqrt(math.pow((current_road_end_loc[0] - current_road_start_loc[0]), 2) +
                               math.pow((current_road_end_loc[1] - current_road_start_loc[1]), 2))

        self.position += (1.0 / road_length) * (1 + self.speed / 100) #Step size
        self.sprite.do(
            MoveTo(
                    (
                        (current_road_start_loc[0] + ((current_road_end_loc[0] - current_road_start_loc[0]) * self.position)),
                        (current_road_start_loc[1] + ((current_road_end_loc[1] - current_road_start_loc[1]) * self.position))
                    ), 0.6)
        )

        self.label.position = (self.sprite.position[0] + 10, self.sprite.position[1] + 10)

    def check_for_bridge(self):
        if self.status == Car_Status.Waiting:
            print("Vehicle " + str(self.index) + " is waiting at the bridge!")
            #return self.handle_cs()

        if ((self.current_road == 2) or (self.current_road == 6) and
            (self.status != Car_Status.Warning and self.status != Car_Status.Waiting)):
            print("Vehicle " + str(self.index) + " is near the bridge!")
            self.status = Car_Status.Warning
            return True
