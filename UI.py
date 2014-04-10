#
# cocos2d
# http://cocos2d.org
#
# This code is so you can run the samples without installing the package
import sys
import os
import random
ri = random.randint
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

import cocos
from cocos.director import director
from cocos.menu import MenuItem
from cocos.draw import Line
from cocos.scene import Scene
import pyglet

class UI:
    class Canvas(cocos.draw.Canvas):
        def render(self):
            x, y = director.get_window_size()

            build_road_map_thingie = [ [[100, 400], [100, 100]], [[100, 400], [200, 250]], [[200, 250], [400, 250]],
                                       [[400, 250], [500, 400]], [[500, 400], [500, 100]], [[500, 100], [400, 250]],
                                       [[100, 100], [200, 250]] ]

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
        def __init__(self):
            super(UI.Layer, self).__init__()

            self.add(UI.Canvas())
            self.schedule(lambda x: 0)
class Entity():
    import threading
    def __init__(self, name, speed, direction):
        self._name = name
        self._speed = speed
        self._direction = direction

    def Start(self):

    def Stop(self):

    def GetLocation(self):

class EntityManager():
    def __init__(self, entityNum, speed, directions):
        self._speed = speed

        for i in range(entityNum):
            entity = Entity(i, speed, directions[i])
            self._entityList.append(entity)

    def Start(self):

    def Stop(self):


def main():
    cocos.director.director.init(caption = "Coolest project ever")

    scene = Scene(UI.Layer())

    cocos.director.director.run(scene)

if __name__ == "__main__":
    main()
