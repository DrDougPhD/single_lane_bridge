# driver.py - Driver of the bridge crossing software. Execute this script to
#  run everything else.
#
# Written by Madeline Cameron and Doug McGeehan
# CS 384 - Distributed Operating Systems
# Spring 2014

import sys
from BridgeMode import BridgeMode
from settings import DEFAULT_NUM_VEHICLES
from settings import DEFAULT_SPEED_CHOICES

# If this script is executed as a command-line script, then let's test to
#  verify that valid parameters have been passed in before doing any
#  time consuming import.s
if __name__ == "__main__":
  usage = """
 $ python {0} BRIDGE_CROSSING_MODE [speed1 [speed2 [...]]]

BRIDGE_CROSSING_MODE can be one of the following:
  0 -- Single vehicle crossing at a time
  1 -- Multiple vehicle crossing if vehicles are traveling in
        same direction and are traveling at the same or lower
        speed of the first vehicle.

speed1-10 indicates the custom initial speed of the vehicles you wish to add.
  The speed must be greater than 0. The number of speed parameters supplied
  as input indicates the number of vehicles you wish to add.
  By default, only five vehicles will be added, with speeds randomly selected
  between the speeds 50, 100, 150, 250, and 400.
  """.format(sys.argv[0])

  # Verify the user has supplied enough command-line arguments
  if len(sys.argv) < 2:
    print("ERROR: Not enough arguments.")
    print(usage)
    sys.exit(1)

  # Verify the user has supplied a valid BridgeMode parameter.
  if int(sys.argv[1]) not in BridgeMode():
    print("ERROR: Incorrect parameter for BRIDGE_CROSSING_MODE := {0}".format(
      sys.argv[1]
    ))
    print(usage)
    sys.exit(2)

  # If the user has supplied custom speeds, verify they are valid speeds.
  if len(sys.argv) > 2:
    speeds = sys.argv[2:]
    for raw_speed in speeds:

      # Verify the parameter is a positive integer.
      try:
        speed = int(raw_speed)
        if speed <= 0:
          raise ValueError

      except ValueError:
        print("USER ERROR: {0} is not a valid speed.".format(raw_speed))
        print(usage)
        sys.exit(3)


# If the execution has made it this far, then the user has supplied valid
#  inputs. We may now spend time performing the necessary imports.

from VehicleManager import VehicleManager
from UI import UI
import cocos
from cocos.director import director
from cocos.scene import Scene
import random
import time
random.seed(time.time())


def main():
    director.init(caption="CS 384 Project")

    # Retrieve command-line arguments
    bridgeMode = int(sys.argv[1])
    speeds = get_speeds(sys.argv)

    manager = VehicleManager(speeds=speeds, mode=bridgeMode)
    layer = UI.Layer(manager)
    print("Setting layer object...")
    manager.layer = layer
    layer.create_speed_label(vehManage=manager)
    layer.create_vehicle_label(vehManage=manager)
    eventHandler = UI.Event_Handler(manager)

    color_layer = cocos.layer.ColorLayer(0,104,10, 0)
    print("Starting scene...")
    scene = Scene(eventHandler, color_layer, layer)
    print("Running scene...")
    director.run(scene)


def get_speeds(argv):
  user_has_specified_custom_speed = (len(argv) > 2)
  if user_has_specified_custom_speed:
    raw_speeds = argv[2:]
    if len(raw_speeds) == 1:
      speeds = [int(raw_speeds[0]) for i in range(DEFAULT_NUM_VEHICLES)]

    else:
      speeds = [int(s) for s in raw_speeds]
      
  else:
    speeds = [
      random.choice(DEFAULT_SPEED_CHOICES) for i in range(DEFAULT_NUM_VEHICLES)
    ]

  return speeds


if __name__ == "__main__":
    # If you run this python script from the command line, then this
    #  if-statement will evaluate to true, in which the main() function
    #  will be executed.
    main()
