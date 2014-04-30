#EntityManager.py
#
#Written by Madeline Cameron and Doug McGeehan
#CS 384 - Distributed Operating Systems
#Spring 2014
#
#Info:
#   Speed is Units per Tick
#   Speed limit is 200 upt

from Vehicle import *
import random, sys, threading, operator, time

class Bridge_Mode():
    One_at_a_Time = -1
    One_direction = 1

class VehicleManager(threading.Thread):
    def __init__(self, vehicleNum, speed, directions, mode):
        threading.Thread.__init__(self)
        self.stopEvent = threading.Event()
        self.speed = speed
        self.vehicleList = []
        self.threadList = []
        self.layer = None
        self.bridge_mode = mode
        self.running = False

        for i in range(vehicleNum):
            vehicle = Vehicle(str(i), speed, directions[i])
            self.vehicleList.append(vehicle)
            print("Vehicle " + str(i) + " added!")

    def set_speed(self, speed):
        self.speed = speed
        self.layer.redraw_speed(speed)

        for vehicle in self.vehicleList:
            vehicle.set_speed(speed)

    def add_vehicle(self, direction):
        #These really need to be more meaningful eventually...
        vehicle = Vehicle(str(len(self.vehicleList)), self.speed, direction)
        self.vehicleList.append(vehicle)
        self.layer.add_vehicle(vehicle)
        self.layer.create_speed_label(vehicle=vehicle)
        self.layer.create_vehicle_label(vehicle=vehicle)

    def run(self):
        self.running = True

        timeStampList = []
        while self.running:
            if self.stopEvent.isSet():
                self.exit()
            for vehicle in self.vehicleList:
                print("Vehicle " + (vehicle.index) + " running!")
                if vehicle.status != Car_Status.Waiting:
                    vehicle.move()
                    vehicle.check_for_bridge()

                if vehicle.timestamp != -1:
                    timeStampList.append([vehicle, vehicle.timestamp])
                    vehicle.timestamp = -1

            if len(timeStampList) > 0:
                #timeStampList.sort(key=operator.itemgetter(2)) #Sort by timestamp / 2nd column
                print("Oldest timestamp: " + str(timeStampList[0][1]) + " from vehicle " + str(timeStampList[0][0].index))

            print("Sleeping for 0.5 seconds")
            time.sleep(0.5)

    def start_threaded(self):
        self.running = True

        for vehicle in self.vehicleList:
            vehicle.start()

        timeStampList = []
        while self.running:
            print("Run")
            for vehicle in self.vehicleList:
                if vehicle.status == "Waiting":
                   timeStampList.append([vehicle, vehicle.timestamp])

            time.sleep(10)

    def stop(self):  #This may not even be needed...
        self.stopEvent.set()
        self.running = False


