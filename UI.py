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
			
            entityList = entityManager.GetEntityList()

            for entity in entityList:
                self.add(entity._sprite)

class Entity():
    import threading
    running = True
    pause = False
    def __init__(self, id, name, speed, direction, pos):
        self._id = id
        self._name = name
        self._speed = speed
        self._direction = direction
        self._pos = pos
        self._status = "Moving"
        self._sprite = cocos.sprite.Sprite('car.png', scale=0.10)
        self._sprite.position = 100, 100

    def GetID(self):
		return self._id
		
    def Start(self):
        pass
		
    def Start(self):
        pass
		
    def Stop(self):
        pass
		
    def GetStatus(self):
        return self._status

    def SetSpeed(self, speed):
        self._speed = speed
		
    def RequestCS(self):
        pass
		
    def GetLocation(self):
        pass

class EntityManager():
    is_event_handler = True

    def __init__(self, entityNum, speed, directions):
        self._speed = speed
        self._entityList = [ ]

        for i in range(entityNum):
            entity = Entity(i, "belh", speed, directions[i], (0, 0))
            self._entityList.append(entity)

    def Start(self):
        for entity in self._entityList:
            entity.Start()

    def Stop(self):
        for entity in self._entityList:
            entity.Stop()

    def GetEntityList(self):
        return self._entityList

    def on_key_press(self, keyp, mod):
        if keyp in (key.SPACE):
            sprite = cocos.sprite.Sprite('start.png')

    def Stop(self):
        pass


def main():
    cocos.director.director.init(caption = "Coolest project ever")
    entManage = EntityManager(2, 10, "boo")
    scene = Scene(UI.Layer(entManage))
    scene = Scene(UI.Layer())
    cocos.director.director.run(scene)


if __name__ == "__main__":
    main()
