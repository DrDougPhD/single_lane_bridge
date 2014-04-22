#EntityManager.py
#
#Written by Madeline Cameron and Doug McGeehan
#CS 384 - Distributed Operating Systems
#Spring 2014
#
#Info:
#   Speed is Units per Tick
#   Speed limit is 200 upt

from Entity import Entity
import random, sys, threading, operator

class Bridge_Mode():
    One_at_a_Time = 0
    One_direction = 1

class EntityManager():
    def __init__(self, entityNum, speed, directions, mode):
        self._speed = speed
        self._entityList = []
        self._threadList = []
        self._layer = None
        self._bridge_mode = mode
        self._running = False

        carNameList = [ "Scion", "Toyota", "Ford", "Lamborgini", "Tesla", "Mercedes", "Mazda", "Chevrolet", "BMW",
                        "Porsche", "Audi", "Volkswagen", "Maserati", "Ferrari", "Subaru", "Lexus", "Honda", "Acura" ]
        for i in range(entityNum):
            randomCar = random.randint(len(carNameList), sys.maxint) % len(carNameList)
            entity = Entity(carNameList[randomCar], speed, directions[i])
            entityThread = threading.Thread(None, entity.main_thread(), "Entity" + str(i))
            self._entityList.append(entity)
            self._threadList.append(entityThread)
            print("Entity " + str(i) + " added!")

    def get_entity_list(self):
        return self._entityList

    def get_speed(self):
        return self._speed

    def set_layer_obj(self, layer):
        self._layer = layer
        print("Layer object set.")

    def set_speed(self, speed):
        self._speed = speed
        self._layer.redraw_speed(speed)

        for entity in self._entityList:
            entity.set_speed(speed)

    def set_bridge_mode(self, mode):
        self._bridge_mode = mode

    def start(self):
        self._running = True

        for entity in self._entityList:
            entity.start()

        for thread in self._threadList:
            thread.start()

        timeStampList = []
        while self._running:
            for entity in self._entityList:
                if entity.get_status() == "Waiting":
                    timeStampList.append([entity, entity.get_timestamp()])

            if len(timeStampList) > 0:
                timeStampList.sort(key=operator.itemgetter(2)) #Sort by timestamp / 2nd column
                print("Oldest timestamp: " + str(timeStampList[0][1]) + " from " + timeStampList[0][0])

    def stop(self):  #This may not even be needed...
        for thread in self._threadList:
            index = self._threadList.index(thread)
            entityObj = self._entityList[index]
            entityObj.stop()
            thread.join()

