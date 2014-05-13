# UI.py
#  Draw the on-screen elements, forward keyboard events, and customize labels
#  when modified.
#
# Written by Madeline Cameron and Doug McGeehan
# CS 384 - Distributed Operating Systems
# Spring 2014


import cocos
from cocos.director import director
from cocos.draw import Line
from pyglet.window import key
import sys
from RoadPoints import RoadPoints


class UI:
    class Canvas(cocos.draw.Canvas):
        def render(self):
            print("Creating canvas...")
            x, y = director.get_window_size()
            color = 255, 255, 255, 255 #Color of lines / roads
            width = 3 #How wide the roads are drawn

            for start, end in RoadPoints.ROADMAP:
                self.set_color(color)
                self.set_stroke_width(width)
                self.move_to(start)
                self.line_to(end)
            print("Road map drawn!")


    class Layer(cocos.layer.Layer):
        def __init__(self, vehicleManager):
            super(UI.Layer, self).__init__()

            self.label_pos_y = 450
            self.label_step = 20
            self.label_color = (255, 255, 255, 255)
            self._vehManage = vehicleManager

            print("Creating layer...")

            self.add(UI.Canvas())
            self.schedule(lambda x: 0)
            print("Canvas added!")

            print("Adding vehicles...")
            for vehicle in vehicleManager.vehicleList:
                self.add(vehicle.sprite)
                print("Vehicle {0} added!".format(vehicle))

            print("Layer created!")

        def redraw_speed(self, vehicle):
            vehicle.speed_label.element.text = str(vehicle.speed)

        def create_speed_label(self, vehicle=None, vehManage=None):
            to_create_list = []
            if vehManage is not None:
                for vehicle in vehManage.vehicleList:
                    to_create_list.append(vehicle)
            else:
                to_create_list.append(vehicle)

            for vehicle in to_create_list:
                print("Creating speed label for vehicle {0}...".format(
                  vehicle
                ))
                speedLabel = cocos.text.Label(
                  "Vehicle {0}'s speed: ".format(vehicle),
                  position=(460, self.label_pos_y),
                  color=self.label_color
                )
                speedText = cocos.text.Label(
                  str(vehicle.speed),
                  position=(600, self.label_pos_y),
                  color=self.label_color
                )
                self.add(speedLabel)
                self.add(speedText)

                self.label_pos_y -= self.label_step

                vehicle.speed_label = speedText

        def create_vehicle_label(self, vehicle=None, vehManage=None):
            to_create_list = []
            if vehManage is not None:
                for vehicle in vehManage.vehicleList:
                    to_create_list.append(vehicle)
            else:
                to_create_list.append(vehicle)

            for vehicle in to_create_list:
                index = self._vehManage.vehicleList.index(vehicle)
                vehicleLabel = cocos.text.Label(
                  str(index),
                  position=(
                    vehicle.sprite.position[0] + 10,
                    vehicle.sprite.position[1] + 10
                  ),
                  color=self.label_color
                )
                vehicle.label = vehicleLabel
                self.add(vehicleLabel)

        def add_vehicle(self, vehicle):
            self.add(vehicle.sprite)
            print("Vehicle {0} added!".format(vehicle))


    class Event_Handler(cocos.layer.Layer):
        # Cocos2D requires this static variable to be set for whichever
        #  class handles human input.
        is_event_handler = True

        def __init__(self, vehicleManage):
            super(UI.Event_Handler, self).__init__()
            self._modifier = None
            self.vehManage = vehicleManage


        def on_close(self):
            sys.exit(0)


        def number_key_pressed(self, keyp):
          if ((keyp >= 65456 and keyp <= 65465) or 
             (keyp >= 48 and keyp <= 57)): #Top-row 1 - 9.
            return True
          else:
            return False


        def get_number_key_pressed(self, keyp):
          if (keyp >= 65456 and keyp <= 65465): #Numpad 1 - 9. Modify vehicle speed
            index = 65456
          elif (keyp >= 48 and keyp <= 57): #Top-row 1 - 9.
            index = 48
          return (keyp - index)


        def on_key_press(self, keyp, mod):
            #Set positive speed modifier
            if keyp == key.NUM_ADD or keyp == key.PLUS or keyp == key.EQUAL:
                print("Speeds will be increased")
                self._modifier = 1

            #Set negative speed modifier
            elif keyp == key.NUM_SUBTRACT or keyp == key.MINUS or keyp == key.UNDERSCORE:
                print("Speeds will be decreased")
                self._modifier = -1

            elif self.number_key_pressed(keyp):
                # Retrieve the number pressed on the keyboard
                index = self.get_number_key_pressed(keyp)
                if self._modifier is not None:
                  if index < len(self.vehManage.vehicleList):
                    new_speed = self.vehManage.vehicleList[index].speed\
                              + (10 * self._modifier)
                    if new_speed > 0:
                      print("Modifying vehicle speed by {0}".format(new_speed))
                      self.vehManage.vehicleList[index].speed = new_speed
                      self.vehManage.layer.redraw_speed(
                        vehicle=self.vehManage.vehicleList[index]
                      )
                    else:
                      print("Speed cannot be 0 or less!")

                  else:
                    print("Please select 0 through {0}".format(
                      len(self.vehManage.vehicleList)-1
                    ))

                else:
                    print("Press - or + to indicate which speed modifier to"
                          " use beforee attempting to modify speed!")

            elif keyp == key.ENTER: #Begin the simulation
                print("Starting simulation...")
                self.vehManage.start()


            elif keyp == key.F1: #Add new vehicle
                if len(self.vehManage.vehicleList) < 10:
                    print("Adding new car...")
                    self.vehManage.add_vehicle()

            elif keyp == key.SPACE:
                print("Pausing?")

            elif keyp == key.ESCAPE: #Exit application gracefully
                print("Goodbye!")
                sys.exit(384) #;D

