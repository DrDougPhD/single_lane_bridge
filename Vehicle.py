#Entity.py
#
#Written by Madeline Cameron and Doug McGeehan
#CS 384 - Distributed Operating Systems
#Spring 2014
#
#Info:
#   Speed is Units per Tick
#   Speed limit is 200 upt

import random, cocos, time, math, threading
from cocos.actions import MoveTo, RotateTo
from UI import RoadPoints


class Car_Status(): #You can totally tell I am a C# developer... can't you?
    Moving = 0      # That's how I would have done it :P
    Waiting = 1
    Warning = 2
    On_Bridge = 3

class Vehicle():
    def __init__(self, name, speed, direction):
        print("Initializing entity " + name + "...")
        random_road = 3
        while random_road == 3: #"Bridge" is road 3 and no one can start there
            random_road = random.randrange(0, 6)
        self.current_road = random_road
        self.timestamp = -1
        self.name = name
        self.speed = speed
        self.direction = direction
        self.status = Car_Status.Moving
        self.sprite = cocos.sprite.Sprite('car.png', scale=0.10)
        if self.current_road % 2 == 0:
            mod = 0
            if self.current_road == 0 or self.current_road == 4:
                mod = -1
            else:
                mod = 1
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
        self.position = 0
        self.running = False
        self.road_map = RoadPoints.ROADMAP
        self.sprite.position = self.road_map[self.current_road][0]
        self.speed_label = None
        print("Vehicle " + name + " initialized!")

    def create_timestamp(self):
        self.timestamp = time.time()

    def move(self):
        #if self._direction == "left":
            #upcomingRoad = (self._current_road + 1) % 3 #(Number of roads - 1) / 2
        #if self._direction == "right":
            #upcomingRoad = (self._current_road - 1) % 3 #(Number of roads - 1) / 2
        print("Moving...")
        if self.position > 1 and self.status != Car_Status.Warning: #If the road has been traveled and not on road 2 or 6
            self.current_road += 1 #Go to the next road
            self.position = 0 #Start over
            if self.current_road % 2 == 0:
                mod = 0
                if self.current_road == 0 or self.current_road == 4:
                    mod = -1
                else:
                    mod = 1
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
        else:
            if self.position > 1 and self.status == Car_Status.Warning:
                self.status = Car_Status.Waiting
                self.create_timestamp() #Fairness should be assured doing it this way,
                                        #assuming system threading is fair, I guess?
        print("C")
        current_road_start_loc = self.road_map[self.current_road][0]
        current_road_end_loc = self.road_map[self.current_road][1]

        road_length = math.sqrt(math.pow((current_road_end_loc[0] - current_road_start_loc[0]), 2) +
                               math.pow((current_road_end_loc[1] - current_road_start_loc[1]), 2))

        self.position += 1.0 / road_length #Step size
        print(str(self.position))
        print(str(((current_road_start_loc[0] + ((current_road_end_loc[0] - current_road_start_loc[0]) * self.position)),
                (current_road_start_loc[1] + ((current_road_end_loc[1] - current_road_start_loc[1]) * self.position)))))
        self.sprite.do(
            MoveTo(
                    (
                        (current_road_start_loc[0] + ((current_road_end_loc[0] - current_road_start_loc[0]) * self.position)),
                        (current_road_start_loc[1] + ((current_road_end_loc[1] - current_road_start_loc[1]) * self.position))
                    ), 0)
        )

    def check_for_bridge(self):
        print("Checking if " + self.name + " is near the bridge!")
        if self.status == Car_Status.Waiting:
            print(self.name + " is waiting at the bridge!")
            #return self.handle_cs()
        if ((self.current_road == 2) or (self.current_road == 6) and self.status != Car_Status.Warning):
            print(self.name + " is near the bridge!")
            self.status = Car_Status.Warning
            return True

    def run(self):
        print("Setting run to True")
        self.running = True
        print("Entity " + self.name + " starting...")
        while self.running:
            print("Entity " + self.name + " running!")
            while self.status != Car_Status.Waiting:
                self.move()
                self.check_for_bridge()
                sleep_time = 10 - (self.speed / 60)
                print("Sleeping for " + str(sleep_time))
                time.sleep(sleep_time) #Yield