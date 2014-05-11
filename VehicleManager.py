#VehicleManager.py
#
#Written by Madeline Cameron and Doug McGeehan
#CS 384 - Distributed Operating Systems
#Spring 2014

from Vehicle import *
from BridgeMode import BridgeMode
import random
import sys
import threading
import operator
import time
class VehicleManager:
    def __init__(self, numVehicles, speed, mode):
        self.speed = speed
        self.vehicleList = []
        self.layer = None
        self.vehicle_class = getVehicleClassByMode(mode)
        self.running = False
        self.tick = 0.5

        for i in range(numVehicles):
            vehicle = self.vehicle_class(
              index=i,
              speed=speed,
            )
            self.vehicleList.append(vehicle)
            print("Vehicle {0} added!".format(vehicle))

        for i in self.vehicleList:
            i.set_other_vehicles(self.vehicleList)

    def set_speed(self, speed):
        self.speed = speed
        self.layer.redraw_speed(speed)

        for vehicle in self.vehicleList:
            vehicle.set_speed(speed)

    def add_vehicle(self):
        vehicle = self.vehicle_class(
          index=len(self.vehicleList),
          speed=self.speed
        )
        self.vehicleList.append(vehicle)
        vehicle.set_other_vehicles(self.vehicleList)

        self.layer.add_vehicle(vehicle)
        self.layer.create_speed_label(vehicle=vehicle)
        self.layer.create_vehicle_label(vehicle=vehicle)


    def start(self):
      print("Starting!!!!!")
      for v in self.vehicleList:
        v.begin()

