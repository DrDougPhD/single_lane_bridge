#UI.py
#
#Written by Madeline Cameron and Doug McGeehan
#CS 384 - Distributed Operating Systems
#Spring 2014
#
#Info:
#   Speed is Units per Tick
#   Speed limit is 250 upt

import sys
import os

import cocos
from cocos.director import director
from cocos.menu import MenuItem
from cocos.draw import Line
from cocos.scene import Scene
import pyglet
from pyglet.window import key
import threading


class UI:
    class Canvas(cocos.draw.Canvas):
        def render(self):
            x, y = director.get_window_size()

            build_road_map_thingie = [
                [[100, 400], [100, 100]],
                [[100, 400], [200, 250]],
                [[200, 250], [400, 250]],
                [[400, 250], [500, 400]],
                [[500, 400], [500, 100]],
                [[500, 100], [400, 250]],
                [[100, 100], [200, 250]]
            ]

            for (startCoord, endCoord) in build_road_map_thingie:
                start = startCoord[0], startCoord[1]
                end = endCoord[0], endCoord[1]
                color = 255, 255, 255, 255
                width = 3
                self.set_color(color)
                self.set_stroke_width(width)
                self.move_to(start)
                self.line_to(end)


    class Layer(cocos.layer.Layer):
        def __init__(self, entityManager):
            super(UI.Layer, self).__init__()

            self.add(UI.Canvas())
            self.schedule(lambda x: 0)

            entityList = entityManager.get_entity_list()

            for entity in entityList:
                self.add(entity.get_sprite())

            speedLabel = cocos.text.Label("Speed: ", position=(545, 450),
                                          color=(200, 200, 200, 200))
            self._speedText = cocos.text.Label(str(entityManager.get_speed()), position=(600, 450),
                                               color=(200, 200, 200, 200))
            self.add(speedLabel)
            self.add(self._speedText)

        def redraw_speed(self, speed):
            self._speedText.element.text = str(speed)


class Entity():
    def __init__(self, name, speed, pos, direction):
        self._name = name
        self._speed = speed
        self._direction = direction
        self._status = "Moving"
        self._sprite = cocos.sprite.Sprite('car.png', scale=0.10)
        self._sprite.position = pos
        self._running = False

    def get_id(self):
        return self._id

    def get_status(self):
        return self._status

    def set_speed(self, speed):
        self._speed = speed

    def request_cs(self):
        pass

    def get_location(self):
        pass

    def get_sprite(self):
        return self._sprite

    def start(self):
        #        running = True
        #        while running:
        #           self._sprite.do(MoveTo())
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
            self.set_speed(self._speed + 10)


def main():
    cocos.director.director.init(caption="Coolest project ever")

    entManage = EntityManager(2, 10, "boo")
    layer = UI.Layer(entManage)
    entManage.set_layer_obj(layer)

    scene = Scene(layer)
    cocos.director.director.run(scene)


if __name__ == "__main__":
    main()
