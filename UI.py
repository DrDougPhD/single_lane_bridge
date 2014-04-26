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
from VehicleManager import *
from cocos.director import director
from cocos.draw import Line
from cocos.scene import Scene
from pyglet.window import key


class RoadPoints:
    NW = 100, 100
    SW = 100, 400
    NE = 500, 100
    SE = 500, 400

    # Intersections of the road with the bridge.
    WEST_BRIDGE_ENTRY = 200, 250
    EAST_BRIDGE_ENTRY = 400, 250

    ROADMAP = [
        [NW, WEST_BRIDGE_ENTRY],
        [NW, SW],
        [SW, WEST_BRIDGE_ENTRY],
        [WEST_BRIDGE_ENTRY, EAST_BRIDGE_ENTRY],
        [EAST_BRIDGE_ENTRY, SE],
        [SE, NE],
        [NE, EAST_BRIDGE_ENTRY],
    ]

class UI:
    class Canvas(cocos.draw.Canvas):
        def render(self):
            print("Creating canvas...")
            x, y = director.get_window_size()
            color = 255, 255, 255, 255
            width = 3

            for start, end in RoadPoints.ROADMAP:
                self.set_color(color)
                self.set_stroke_width(width)
                self.move_to(start)
                self.line_to(end)
            print("Road map drawn!")

    class Layer(cocos.layer.Layer):
        def __init__(self, vehicleManager):
            super(UI.Layer, self).__init__()

            print("Creating layer...")

            self.add(UI.Canvas())
            self.schedule(lambda x: 0)
            print("Canvas added!")

            print("Adding vehicles...")
            for vehicle in vehicleManager.vehicleList:
                self.add(vehicle.sprite)
                print("Vehicle " + vehicle.name + " added!")

            print("Layer created!")

        def redraw_speed(self, vehicle):
            print("Redrawing speed...")
            vehicle.speed_label.element.text = str(vehicle.speed)

        def create_speed_label(self, vehicle):
            print("Creating speed label for " + vehicle.name + "...")
            speedLabel = cocos.text.Label("Default: ", position=(545, 450),
                                          color=(200, 200, 200, 200))
            speedText = cocos.text.Label(str(vehicle.speed), position=(600, 450),
                                               color=(200, 200, 200, 200))
            self.add(speedLabel)
            self.add(speedText)

            vehicle.speed_label = speedText

        def add_vehicle(self, vehicle):
            self.add(vehicle.sprite)
            print("Vehicle " + vehicle.name + " added!")

    class Key_Handler(cocos.layer.Layer):
        is_event_handler = True

        def __init__(self, vehicleManage):
            super(UI.Key_Handler, self).__init__()

            self.vehManage = vehicleManage

        def on_key_press(self, keyp, mod):
            if keyp == key.SPACE:
                speed_increase = self.vehManage.speed + 10
                print("Increasing speed to: " + str(speed_increase))
                self.vehManage.set_speed(speed_increase)
            if keyp == key.ENTER:
                print("Starting simulation...")
                for vehicle in self.vehManage.vehicleList:
                    vehicle.move()
            if keyp == key.F1:
                print("Adding new car...")
                self.vehManage.add_vehicle("left")


def main():
    cocos.director.director.init(caption="CS 384 Project")

    directions = ["left", "right"]
    vehManage = VehicleManager(2, 10, directions, Bridge_Mode.One_at_a_Time)
    layer = UI.Layer(vehManage)
    print("Setting layer object...")
    vehManage.layer = layer

    keyHandler = UI.Key_Handler(vehManage)

    print("Starting scene...")
    scene = Scene(layer, keyHandler)
    print("Running scene...")
    cocos.director.director.run(scene)
    print("Scene running!")
    print("Goodbye!")


if __name__ == "__main__":
    # If you run this python script from the command line, then this
    #  if-statement will evaluate to true, in which the main() function
    #  will be executed.
    main()