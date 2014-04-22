#Entity.py
#
#Written by Madeline Cameron and Doug McGeehan
#CS 384 - Distributed Operating Systems
#Spring 2014
#
#Info:
#   Speed is Units per Tick
#   Speed limit is 200 upt

import random, cocos, time, math
from cocos.actions import MoveTo, Rotate


class Car_Status(): #You can totally tell I am a C# developer... can't you?
    Moving = 0
    Waiting = 1
    Warning = 2
    On_Bridge = 3

class Entity():
    def __init__(self, name, speed, direction):
        print("Initializing entity " + name + "...")
        random_road = 3
        while random_road == 3: #"Bridge" is road 3 and no one can start there
            random_road = random.randrange(0, 6)
        self._current_road = random_road
        self._timestamp = -1
        self._name = name
        self._speed = speed
        self._direction = direction
        self._status = Car_Status.Moving
        self._sprite = cocos.sprite.Sprite('car.png', scale=0.10)
        self._position = 0
        self._running = False
        self._road_map = [
                [[100, 100], [200, 250]],
                [[100, 100], [100, 400]],
                [[100, 400], [200, 250]],
                [[200, 250], [400, 250]],
                [[400, 250], [500, 400]],
                [[500, 400], [500, 100]],
                [[500, 100], [400, 250]],
            ]
        self._sprite.position = self._road_map[self._current_road][0]
        print("Entity " + name + " initialized!")

    def get_name(self):
        return self._name

    def get_status(self):
        return self._status

    def set_speed(self, speed):
        self._speed = speed

    def get_location(self):
        return self._sprite.position

    def get_sprite(self):
        return self._sprite

    def get_timestamp(self):
        return self._timestamp

    def give_bridge_ticket(self):
        self._status = Car_Status.On_Bridge
        pass

    def create_timestamp(self):
        self._timestamp = time.time()

    def move(self):
        #if self._direction == "left":
            #upcomingRoad = (self._current_road + 1) % 3 #(Number of roads - 1) / 2
        #if self._direction == "right":
            #upcomingRoad = (self._current_road - 1) % 3 #(Number of roads - 1) / 2

        if self._position > 1 and self._status != Car_Status.Warning: #If the road has been traveled and not on road 2 or 6
            self._current_road += 1 #Go to the next road
            self._position = 0 #Start over
        else:
            if self._position > 1 and self._status == Car_Status.Warning:
                self._status = Car_Status.Waiting
                self.create_timestamp() #Fairness should be assured doing it this way,
                                        #assuming system threading is fair, I guess?

        current_road_start_loc = self._road_map[self._current_road][0]
        current_road_end_loc = self._road_map[self._current_road][1]
        loc = self.get_location()

        road_length = math.sqrt(math.pow((current_road_end_loc[0] - current_road_start_loc[0]), 2) +
                               math.pow((current_road_end_loc[1] - current_road_start_loc[1]), 2))

        self._sprite.do(
            MoveTo(
                    (
                        (loc[0] + ((current_road_end_loc[0] - current_road_start_loc[0]) * (self._position[0] * self._speed))),
                        (loc[1] + ((current_road_end_loc[1] - current_road_start_loc[1]) * (self._position[1] * self._speed)))
                    ), 1)
        )

    def check_for_bridge(self):
        print("Checking if " + self._name + " is near the bridge!")
        if self._status == Car_Status.Waiting:
            print(self._name + " is waiting at the bridge!")
            return self.handle_cs()
        if ((self._current_road == 2) or (self._current_road == 6) and self._status != Car_Status.Warning):
            print(self._name + " is near the bridge!")
            self._status = Car_Status.Warning
            return True

    def start(self):
        print("Setting run to True")
        self._running = True

    def main_thread(self):
        print("Entity " + self._name + " starting...")
        while self._running:
            print("Entity " + self._name + " running!")
            while self._status != Car_Status.Waiting:
                print("Moving!")
                self.move()
                self.check_for_bridge()
        return