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

class VehicleManager():
    def __init__(self, entityNum, speed, directions, mode):
        self.speed = speed
        self.vehicleList = []
        self.threadList = []
        self.layer = None
        self.bridge_mode = mode
        self.running = False

        #These really need to be more meaningful eventually...
        carNameList = [ "Scion", "Toyota", "Ford", "Lamborgini", "Tesla", "Mercedes", "Mazda", "Chevrolet", "BMW",
                        "Porsche", "Audi", "Volkswagen", "Maserati", "Ferrari", "Subaru", "Lexus", "Honda", "Acura" ]
        for i in range(entityNum):
            randomCar = random.randint(len(carNameList), sys.maxint) % len(carNameList)
            vehicle = Vehicle(carNameList[randomCar], speed, directions[i])
            self.vehicleList.append(vehicle)
            print("Vehicle " + str(i) + " added!")

    def set_speed(self, speed):
        self.speed = speed
        self.layer.redraw_speed(speed)

        for vehicle in self.vehicleList:
            vehicle.set_speed(speed)

    def add_vehicle(self, direction):
        #These really need to be more meaningful eventually...
        carNameList = [ "Scion", "Toyota", "Ford", "Lamborgini", "Tesla", "Mercedes", "Mazda", "Chevrolet", "BMW",
                        "Porsche", "Audi", "Volkswagen", "Maserati", "Ferrari", "Subaru", "Lexus", "Honda", "Acura" ]
        randomCar = random.randint(len(carNameList), sys.maxint) % len(carNameList)
        vehicle = Vehicle(carNameList[randomCar], self.speed, direction)
        self.vehicleList.append(vehicle)
        self.layer.add_vehicle(vehicle)

    def start_round_robin(self):
        self.running = True

        timeStampList = []
        while self.running:
            for vehicle in self.vehicleList:
                print("Entity " + vehicle.name + " running!")
                if vehicle.status != Car_Status.Waiting:
                    vehicle.move()
                    vehicle.check_for_bridge()

                if vehicle.timestamp != -1:
                    timeStampList.append([vehicle, vehicle.timestamp])
                    vehicle.timestamp = -1

            if len(timeStampList) > 0:
                timeStampList.sort(key=operator.itemgetter(2)) #Sort by timestamp / 2nd column
                print("Oldest timestamp: " + str(timeStampList[0][1]) + " from " + timeStampList[0][0])

            sleep_time = 10 - (self.speed / 60)
            print("Sleeping for " + str(sleep_time))
            time.sleep(sleep_time) #Yield

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
        for thread in self._threadList:
            index = self._threadList.index(thread)
            entityObj = self.vehicleList[index]
            entityObj.stop()
            thread.join()


