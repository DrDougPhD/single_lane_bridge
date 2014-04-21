#UI.py
#
#Written by Madeline Cameron and Doug McGeehan
#CS 384 - Distributed Operating Systems
#Spring 2014
#
#Info:
#   Speed is Units per Tick
#   Speed limit is 200 upt

import sys
import os

import cocos, math, time
from cocos.director import director
from cocos.menu import MenuItem
from cocos.draw import Line
from cocos.scene import Scene
from cocos.actions import MoveTo, Rotate
import pyglet
from pyglet.window import key
import threading


class Car_Status(): #You can totally tell I am a C# developer... can't you?
    Moving = 0
    Waiting = 1
    Warning = 2
    On_Bridge = 3

class UI:
    class Canvas(cocos.draw.Canvas):
        def render(self):
            print "Creating canvas..."
            x, y = director.get_window_size()

            roadmap = [
                [[100, 100], [200, 250]],
                [[100, 100], [100, 400]],
                [[100, 400], [200, 250]],
                [[200, 250], [400, 250]],
                [[400, 250], [500, 400]],
                [[500, 400], [500, 100]],
                [[500, 100], [400, 250]],
            ]

            for (startCoord, endCoord) in roadmap:
                start = startCoord[0], startCoord[1]
                end = endCoord[0], endCoord[1]
                color = 255, 255, 255, 255
                width = 3
                self.set_color(color)
                self.set_stroke_width(width)
                self.move_to(start)
                self.line_to(end)
            print "Road map drawn!"

    class Layer(cocos.layer.Layer):
        def __init__(self, entityManager):
            super(UI.Layer, self).__init__()

            print "Creating layer..."

            self.add(UI.Canvas())
            self.schedule(lambda x: 0)
            print "Canvas added!"

            print "Adding entities..."
            entityList = entityManager.get_entity_list()
            for entity in entityList:
                self.add(entity.get_sprite())
                print "Entity " + entity.get_name() + " added!"

            print "Creating assorted UI elements..."
            speedLabel = cocos.text.Label("Speed: ", position=(545, 450),
                                          color=(200, 200, 200, 200))
            self._speedText = cocos.text.Label(str(entityManager.get_speed()), position=(600, 450),
                                               color=(200, 200, 200, 200))
            print "Adding assorted UI elements..."
            self.add(speedLabel)
            self.add(self._speedText)

            print "Layer created!"

        def redraw_speed(self, speed):
            print "Redrawing speed..."
            self._speedText.element.text = str(speed)


class Entity():
    def __init__(self, name, speed, pos, direction):
        print "Initializing entity " + name + "..."
        import random
        random_road = 3
        while random_road != 3: #"Bridge" is road 3 and no one can start there
            random_road = random.randrange(0, 6)
        del random
        self._current_road = random_road
        self._timestamp = -1
        self._name = name
        self._speed = speed
        self._direction = direction
        self._status = Car_Status.Moving
        self._sprite = cocos.sprite.Sprite('car.png', scale=0.10)
        self._position = pos
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
        print "Entity " + name + " initialized!"

    def get_name(self):
        return self._name

    def get_status(self):
        return self._status

    def set_speed(self, speed):
        self._speed = speed

    def handle_cs(self):
        self._timestamp = time.time() #Make a timestamp of "ticket request"
        running = False

        return False

    def get_location(self):
        return self._sprite.position

    def get_sprite(self):
        return self._sprite

    def get_timestamp(self):
        return self._timestamp

    def give_bridge_ticket(self):
        self._has_ticket = True #Can go over the bridge
        pass

    def move(self):
        #if self._direction == "left":
            #upcomingRoad = (self._current_road + 1) % 3 #(Number of roads - 1) / 2
        #if self._direction == "right":
            #upcomingRoad = (self._current_road - 1) % 3 #(Number of roads - 1) / 2

        if self._position > 1 and self._status != Car_Status.Warning: #If the road has been traveled and not on road 2 or 6
            self._current_road += 1 #Go to the next road
            self.position = 0 #Start over

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
        if self._status == Car_Status.Waiting:
            return self.handle_cs()
        if ((self._current_road == 2) or (self._current_road == 6) and self._status != Car_Status.Warning):
            self._status = Car_Status.Warning
            return True

    def start(self):
        #running = True
        print "Entity " + self._name + " starting..."
        while self._running:
            self.move()
            self.check_for_bridge()
        pass

    def stop(self):
        pass


class EntityManager():
    is_event_handler = True

    def __init__(self, entityNum, speed, directions):
        self._speed = speed
        self._entityList = []
        self._threadList = []
        self._layer = None

        for i in range(entityNum):
            entity = Entity("bleh", speed, (100, 100), directions[i])
            entityThread = threading.Thread(None, entity.start(), "Entity" + str(i))
            self._entityList.append(entity)
            self._threadList.append(entityThread)
            print "Entity " + str(i) + " added!"

    def get_entity_list(self):
        return self._entityList

    def get_speed(self):
        return self._speed

    def set_layer_obj(self, layer):
        self._layer = layer

    def set_speed(self, speed):
        self._speed = speed
        self._layer.redraw_speed()

        for entity in self._entityList:
            entity.set_speed(speed)

    def start(self):
        for thread in self._threadList:
            thread.start()

    def stop(self):  #This may not even be needed...
        for thread in self._threadList:
            index = self._threadList.index(thread)
            entityObj = self._entityList[index]
            entityObj.stop()
            thread.join()

    def on_key_press(self, keyp, mod):
        if keyp in (key.SPACE):
            speed_increase = self._speed + 10
            print "Increasing speed to " + str(speed_increase) + "..."
            self.set_speed(speed_increase)
        if keyp in (key.ENTER):
            print "Starting simulation..."
            self.start()


def main():
    cocos.director.director.init(caption="CS 384 Project")

    directions = [ "left", "right" ]
    entManage = EntityManager(2, 10, directions)
    layer = UI.Layer(entManage)
    print "Setting layer object..."
    entManage.set_layer_obj(layer)

    print "Starting scene..."
    scene = Scene(layer)
    print "Running scene..."
    cocos.director.director.run(scene)
    print "Scene running!"


if __name__ == "__main__":
    main()
