#UI.py
#
#Written by Madeline Cameron and Doug McGeehan
#CS 384 - Distributed Operating Systems
#Spring 2014

import sys
from BridgeMode import BridgeMode
# If this script is executed as a command-line script, then let's test to
#  verify that valid parameters have been passed in before doing any
#  time consuming import.s
if __name__ == "__main__":
  usage = """
 $ python {0} BRIDGE_CROSSING_MODE

BRIDGE_CROSSING_MODE can be one of the following:
  0 -- Single vehicle crossing at a time
  1 -- Multiple vehicle crossing if vehicles are traveling in
        same direction and are traveling at the same or lower
        speed of the first vehicle.

  """.format(sys.argv[0])

  if len(sys.argv) < 2:
    print("Not enough arguments. Please specify the bridge-crossing mode.")
    print(usage)
    sys.exit(1)

  if int(sys.argv[1]) not in BridgeMode():
    print("Incorrect parameter for BRIDGE_CROSSING_MODE := {0}".format(
      sys.argv[1]
    ))
    print(usage)
    sys.exit(2)

# If the execution has made it this far, then the user has supplied valid
#  inputs. We may now spend time performing the necessary imports.

from VehicleManager import VehicleManager
from UI import UI
import cocos
from cocos.director import director
from threading import Thread
from cocos.scene import Scene

def main():
    director.init(caption="CS 384 Project")
    bridgeMode = int(sys.argv[1])

    vehManage = VehicleManager(
      numVehicles=2,
      speed=100,
      mode=bridgeMode
    )
    layer = UI.Layer(vehManage)
    print("Setting layer object...")
    vehManage.layer = layer
    layer.create_speed_label(vehManage=vehManage)
    layer.create_vehicle_label(vehManage=vehManage)
    eventHandler = UI.Event_Handler(vehManage)

    color_layer = cocos.layer.ColorLayer(0,104,10, 0)
    print("Starting scene...")
    scene = Scene(eventHandler, color_layer, layer)
    print("Running scene...")
    UIThread = Thread(group=None, target=director.run(scene))
    UIThread.start()


if __name__ == "__main__":
    # If you run this python script from the command line, then this
    #  if-statement will evaluate to true, in which the main() function
    #  will be executed.
    main()
