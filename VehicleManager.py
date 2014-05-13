# VehicleManager.py
#  Manage the creation, addition, and running of vehicles.
#
# Written by Madeline Cameron and Doug McGeehan
# CS 384 - Distributed Operating Systems
# Spring 2014

from Vehicle import getVehicleClassByMode
from settings import DEFAULT_SPEED_CHOICES
import random

class VehicleManager:
    def __init__(self, speeds, mode):
        self.vehicleList = []
        self.layer = None
        self.running = False

        # Based on the bridge-crossing mode, select the appropriate Vehicle
        #  class to initialize the Vehicles. The vehicle classes have
        #  different bridge-access-requesting algorithms implemented.
        self.vehicle_class = getVehicleClassByMode(mode)

        for s in speeds:
            vehicle = self.vehicle_class(speed=s)
            self.vehicleList.append(vehicle)
            print("Vehicle {0} added!".format(vehicle))

        # Each vehicle needs to be aware of all other vehicles in order to
        #  broadcast requests.
        for v in self.vehicleList:
            v.set_other_vehicles(self.vehicleList)

    
    def add_vehicle(self):
        # Create a new vehicle dynamically before movement of the vehicles
        #  begins.
        if self.running:
          print("You cannot add a new vehicle while the simulation is"
                " running! Please restart the program and add your vehicles"
                " before starting the simulation")

        else:
          vehicle = self.vehicle_class(
            speed=random.choice(DEFAULT_SPEED_CHOICES)
          )
          self.vehicleList.append(vehicle)
          vehicle.set_other_vehicles(self.vehicleList)

          self.layer.add_vehicle(vehicle)
          self.layer.create_speed_label(vehicle=vehicle)


    def start(self):
      # Begin the simulation!
      print("Starting!!!!!")
      self.running = True
      for v in self.vehicleList:
        v.begin()

