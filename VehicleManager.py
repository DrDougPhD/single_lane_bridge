#VehicleManager.py
#
#Written by Madeline Cameron and Doug McGeehan
#CS 384 - Distributed Operating Systems
#Spring 2014

from Vehicle import *
import random
import sys
import threading
import operator
import time

class Bridge_Mode():
    One_at_a_Time = -1
    One_direction = 1

class VehicleManager:#(threading.Thread):
    def __init__(self, vehicleNum, speed, directions, mode):
        #threading.Thread.__init__(self)
        self.stopEvent = threading.Event()
        self.speed = speed
        self.vehicleList = []
        self.layer = None
        self.bridge_mode = mode
        self.running = False
        self.tick = 0.5

        for i in range(vehicleNum):
            vehicle = Vehicle(str(i), speed, directions[i])
            self.vehicleList.append(vehicle)
            print("Vehicle " + str(i) + " added!")

        for i in self.vehicleList:
            i.set_other_vehicles(self.vehicleList)

    def set_speed(self, speed):
        self.speed = speed
        self.layer.redraw_speed(speed)

        for vehicle in self.vehicleList:
            vehicle.set_speed(speed)

    def add_vehicle(self, direction):
        vehicle = Vehicle(str(len(self.vehicleList)), self.speed, direction)
        # Notify all other vehicles of new vehicle.
        vehicle.set_other_vehicles(self.vehicleList)
        for v in self.vehicleList:
          v.inform_of_another_vehicle(v)

        self.vehicleList.append(vehicle)
        self.layer.add_vehicle(vehicle)
        self.layer.create_speed_label(vehicle=vehicle)
        self.layer.create_vehicle_label(vehicle=vehicle)


    def start(self):
      print("Starting!!!!!")
      for v in self.vehicleList:
        v.begin()


    def run(self):
        self.running = True

        timeStampList = []
        while self.running:
            if self.stopEvent.isSet(): #Look for exit event to be set
                self.exit()

            for vehicle in self.vehicleList:
                if vehicle.status != Car_Status.Waiting:
                    vehicle.move()
                    vehicle.check_for_bridge()
                else:
                    print("Vehicle " + str(vehicle.index) + " waiting!")

                if vehicle.timestamp != -1:
                    timeStampList.append([vehicle, vehicle.timestamp])
                    vehicle.timestamp = -1

            if len(timeStampList) > 0:
                #timeStampList.sort(key=operator.itemgetter(2)) #Sort by timestamp / 2nd column
                print("Oldest timestamp: " + str(timeStampList[0][1]) + " from vehicle " + str(timeStampList[0][0].index))

            time.sleep(0.5) #Arbitrary

    def stop(self):  #This may not even be needed...
        self.stopEvent.set()
        self.running = False


