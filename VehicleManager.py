#VehicleManager.py
#
#Written by Madeline Cameron and Doug McGeehan
#CS 384 - Distributed Operating Systems
#Spring 2014

from Vehicle import getVehicleClassByMode
class VehicleManager:
    def __init__(self, speeds, mode):
        self.vehicleList = []
        self.layer = None
        self.vehicle_class = getVehicleClassByMode(mode)

        for s in speeds:
            vehicle = self.vehicle_class(speed=s)
            self.vehicleList.append(vehicle)
            print("Vehicle {0} added!".format(vehicle))

        for v in self.vehicleList:
            v.set_other_vehicles(self.vehicleList)

    
    def add_vehicle(self):
        vehicle = self.vehicle_class(
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

