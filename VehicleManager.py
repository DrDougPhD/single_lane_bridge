#EntityManager.py
#
#Written by Madeline Cameron and Doug McGeehan
#CS 384 - Distributed Operating Systems
#Spring 2014
#
#Info:
#   Speed is Units per Tick
#   Speed limit is 200 upt

from Vehicle import Entity
import random, sys, threading, operator, time

class Bridge_Mode():
    One_at_a_Time = 0
    One_direction = 1

class VehicleManager():
    def __init__(self, entityNum, speed, directions, mode):
        self.speed = speed
        self.vehicleList = []
        self.threadList = []
        self.layer = None
        self.bridge_mode = mode
        self._running = False

        carNameList = [ "Scion", "Toyota", "Ford", "Lamborgini", "Tesla", "Mercedes", "Mazda", "Chevrolet", "BMW",
                        "Porsche", "Audi", "Volkswagen", "Maserati", "Ferrari", "Subaru", "Lexus", "Honda", "Acura" ]
        for i in range(entityNum):
            randomCar = random.randint(len(carNameList), sys.maxint) % len(carNameList)
            entity = Entity(carNameList[randomCar], speed, directions[i])
            self.entityList.append(entity)
            print("Vehicle " + str(i) + " added!")

    def set_speed(self, speed):
        self._speed = speed
        self._layer.redraw_speed(speed)

        for vehicle in self.vehicleList:
            vehicle.set_speed(speed)

    def start(self):
        self._running = True

        for vehicle in self.vehicleList:
            vehicle.start()

        timeStampList = []
        while self._running:
            print("Run")
            for vehicle in self.vehicleList:
                if vehicle.status == "Waiting":
                    timeStampList.append([vehicle, vehicle.timestamp])

            if len(timeStampList) > 0:
                timeStampList.sort(key=operator.itemgetter(2)) #Sort by timestamp / 2nd column
                print("Oldest timestamp: " + str(timeStampList[0][1]) + " from " + timeStampList[0][0])
            time.sleep(10)

    def stop(self):  #This may not even be needed...
        for thread in self._threadList:
            index = self._threadList.index(thread)
            entityObj = self.vehicleList[index]
            entityObj.stop()
            thread.join()

