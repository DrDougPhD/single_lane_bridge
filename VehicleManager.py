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
    One_at_a_Time = 0
    One_direction = 1

class VehicleManager:
    def __init__(self, numVehicles, speed, directions, mode):
        #threading.Thread.__init__(self)
        self.stopEvent = threading.Event()
        self.speed = speed
        self.vehicleList = []
        self.layer = None
        self.bridge_mode = mode
        self.running = False
        self.tick = 0.5

        for i in range(numVehicles):
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
        self.vehicleList.append(vehicle)
        vehicle.set_other_vehicles(self.vehicleList)

        self.layer.add_vehicle(vehicle)
        self.layer.create_speed_label(vehicle=vehicle)
        self.layer.create_vehicle_label(vehicle=vehicle)


    def start(self):
      print("Starting!!!!!")
      for v in self.vehicleList:
        v.begin()

