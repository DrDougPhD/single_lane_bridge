#UI.py
#
#Written by Madeline Cameron and Doug McGeehan
#CS 384 - Distributed Operating Systems
#Spring 2014
#
#Info:
#   Speed is Units per Tick
#   Speed limit is 200 upt


import cocos
from EntityManager import EntityManager
from EntityManager import Bridge_Mode
from cocos.director import director
from cocos.draw import Line
from cocos.scene import Scene
from pyglet.window import key

class UI:
    class Canvas(cocos.draw.Canvas):
        def render(self):
            print("Creating canvas...")
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
            print("Road map drawn!")

    class Layer(cocos.layer.Layer):
        def __init__(self, entityManager):
            super(UI.Layer, self).__init__()

            print("Creating layer...")

            self.add(UI.Canvas())
            self.schedule(lambda x: 0)
            print("Canvas added!")

            print("Adding entities...")
            entityList = entityManager.get_entity_list()
            for entity in entityList:
                self.add(entity.get_sprite())
                print("Entity " + entity.get_name() + " added!")

            print("Creating assorted UI elements...")
            speedLabel = cocos.text.Label("Speed: ", position=(545, 450),
                                          color=(200, 200, 200, 200))
            self._speedText = cocos.text.Label(str(entityManager.get_speed()), position=(600, 450),
                                               color=(200, 200, 200, 200))
            print("Adding assorted UI elements...")
            self.add(speedLabel)
            self.add(self._speedText)

            print("Layer created!")

        def redraw_speed(self, speed):
            print("Redrawing speed...")
            self._speedText.element.text = str(speed)

    class Key_Handler(cocos.layer.Layer):
        is_event_handler = True

        def __init__(self, entityManager):
            super(UI.Key_Handler, self).__init__()

            self._entManager = entityManager

        def on_key_press(self, keyp, mod):
            if keyp == key.SPACE:
                speed_increase = self._entManager.get_speed() + 10
                print("Increasing speed to: " + str(speed_increase))
                self._entManager.set_speed(speed_increase)
            if keyp == key.ENTER:
                print("Starting simulation...")
                self._entManager.start()
def main():
    cocos.director.director.init(caption="CS 384 Project")

    directions = [ "left", "right" ]
    entManage = EntityManager(2, 10, directions, Bridge_Mode.One_at_a_Time)
    layer = UI.Layer(entManage)
    print("Setting layer object...")
    entManage.set_layer_obj(layer)

    keyHandler = UI.Key_Handler(entManage)

    print("Starting scene...")
    scene = Scene(layer, keyHandler)
    print("Running scene...")
    cocos.director.director.run(scene)
    print("Scene running!")


if __name__ == "__main__":
    main()
