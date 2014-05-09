#Vehicle.py
#
#Written by Madeline Cameron and Doug McGeehan
#CS 384 - Distributed Operating Systems
#Spring 2014

import random, cocos, time, math, threading
from cocos.actions import MoveTo, RotateTo
from UI import RoadPoints
from cocos.actions import CallFunc

def duration(src, dst, speed):
  return 1


# Precondition: The process which called this is waiting for the token to
#  enter the critical section.
def get_movement_path(starting_point, vehicle):
  """When a process is given the token for entry on the bridge, it will
  be permitted to cross the bridge and drive through the town."""

  if starting_point == RoadPoints.W:
    # Cross the bridge from West to East.
    #  It is assumed the car is currently at RoadPoints.W
    #  W -> E -> NE -> SE -> E
    return (
      MoveTo(RoadPoints.E, duration(starting_point, RoadPoints.E, vehicle.speed)) + \
      #Rotate() + \
      CallFunc(vehicle.leave_bridge) + \
      get_town_travel_path(RoadPoints.E, vehicle.speed)
    )

  elif starting_point == RoadPoints.E:
    # Cross the bridge from East to West.
    #  It is assumed the car is currently at RoadPoints.W
    #  E -> W -> SW -> NW -> W
    return (
      MoveTo(RoadPoints.W, duration(starting_point, RoadPoints.W, vehicle.speed)) + \
      #Rotate() + \
      CallFunc(vehicle.leave_bridge) + \
      get_town_travel_path(RoadPoints.W, vehicle.speed)
    )


def get_town_travel_path(starting_point, speed):
  """When a process is given the token for entry on the bridge, it will
  be permitted to cross the bridge and drive through the town."""

  if starting_point == RoadPoints.E:
    # Travel the Eastern Town.
    #  It is assumed the car is currently at RoadPoints.E
    #  E -> NE -> SE -> E
    return (
      #Rotate() + \
      MoveTo(RoadPoints.NE, duration(RoadPoints.E, RoadPoints.NE, speed)) + \
      #Rotate() + \
      MoveTo(RoadPoints.SE, duration(RoadPoints.NE, RoadPoints.SE, speed)) + \
      #Rotate() + \
      MoveTo(RoadPoints.E, duration(RoadPoints.SE, RoadPoints.E, speed))
    )

  elif starting_point == RoadPoints.NE:
    # Travel the Eastern Town.
    #  It is assumed the car is currently at RoadPoints.E
    #  NE -> SE -> E
    return (
      #Rotate() + \
      MoveTo(RoadPoints.SE, duration(RoadPoints.NE, RoadPoints.SE, speed)) + \
      #Rotate() + \
      MoveTo(RoadPoints.E, duration(RoadPoints.SE, RoadPoints.E, speed))
    )

  elif starting_point == RoadPoints.SE:
    # Travel the Eastern Town.
    #  It is assumed the car is currently at RoadPoints.E
    #  SE -> E
    return (
      #Rotate() + \
      MoveTo(RoadPoints.E, duration(RoadPoints.SE, RoadPoints.E, speed))
    )

  elif starting_point == RoadPoints.W:
    # Travel the Western Town.
    #  It is assumed the car is currently at RoadPoints.W
    #  W -> SW -> NW -> W
    return (
      #Rotate() + \
      MoveTo(RoadPoints.SW, duration(RoadPoints.W, RoadPoints.SW, speed)) + \
      #Rotate() + \
      MoveTo(RoadPoints.NW, duration(RoadPoints.SW, RoadPoints.NW, speed)) + \
      #Rotate() + \
      MoveTo(RoadPoints.W, duration(RoadPoints.NW, RoadPoints.W, speed))
    )

  elif starting_point == RoadPoints.SW:
    # Travel the Western Town.
    #  SW -> NW -> W
    return (
      #Rotate() + \
      MoveTo(RoadPoints.NW, duration(RoadPoints.SW, RoadPoints.NW, speed)) + \
      #Rotate() + \
      MoveTo(RoadPoints.W, duration(RoadPoints.NW, RoadPoints.W, speed))
    )

  elif starting_point == RoadPoints.NW:
    # Travel the Western Town.
    #  NW -> W
    return (
      #Rotate() + \
      MoveTo(RoadPoints.W, duration(RoadPoints.NW, RoadPoints.W, speed))
    )


class Car_Status(): #You can totally tell I am a C# developer... can't you?
    Moving = 0      # That's how I would have done it :P
    Waiting = 1
    Warning = 2
    On_Bridge = 3

class Vehicle():
    def __init__(self, index, speed, direction):
        print("Initializing vehicle " + str(index) + "...")

        random_road = random.choice([0, 1, 2, 4, 5, 6]) #"Bridge" is road 3 and no one can start there
        self.buffered_requests = []
        self.is_on_bridge = False
        self.current_road = random_road
        self.timestamp = None
        self.index = index
        self.speed = speed
        self.direction = direction
        self.status = Car_Status.Moving
        self.position = 0
        self.road_map = RoadPoints.ROADMAP
        self.label = None
        self.sprite = cocos.sprite.Sprite(
          'car2.png',
          scale=0.10,
          color=[random.randrange(0, 255) for i in range(3)]
        ) #Pick a random color
        self.sprite.position = self.road_map[self.current_road][0]
        """
        if self.current_road % 2 == 0: #Vehicle rotation
            mod = 0
            if self.current_road == 0 or self.current_road == 4:
                if self.current_road == 4:
                    mod = -1
                else:
                    mod = -4.2142857
            else:
                if self.current_road == 2:
                    mod = 1
                else:
                    mod = 4.2142857
            self.sprite.do(RotateTo(mod*56, 0))
        if self.current_road == 1 or self.current_road == 5:
            mod = 0
            if self.current_road == 1:
                mod = -1
            else:
                mod = 1
            self.sprite.do(RotateTo(mod*90, 0))
        if self.current_road == 3:
            self.sprite.do(RotateTo(0, 0))
        """
        print("Vehicle " + str(index) + " initialized!")


    def begin(self):
      drive_path = get_town_travel_path(self.road_map[self.current_road][0], self)
      request_bridge_access = CallFunc(self.request_access_to_bridge)
      self.sprite.do(drive_path + request_bridge_access) 


    def set_other_vehicles(self, other_vehicles):
      self.other_vehicles = []
      for f in other_vehicles:
        if self != f:
          self.other_vehicles.append(f)


    def create_timestamp(self):
        self.timestamp = time.time()


    def request_access_to_bridge(self):
      # Record the time and reset the acknowledgement tracker.
      now = time.time()
      self.timestamp = now
      print("{0} is requesting bridge access".format(self.index))
      self.acknowledgements = {v:False for v in self.other_vehicles}

      # As per Ricart & Agrawala's algorithm, broadcast a timestamped request
      # to all other vehicles.
      for c in self.other_vehicles:
        print("{0} sent request to {1}".format(self.index, c.index))
        c.request(self, now)


    def request(self, requester, t):
      # As per Ricart & Agrawala's algorithm, the requester has broadcast a
      #  timestamped request to all vehicles. This vehicle has received the
      #  request and checks if it needs access to the bridge. Return an 
      #  acknowledgement if:
      #    1. This vehicle does not need access to the bridge
      #    2. This vehicle's request occurred later than the other vehicle
      # If we are already on the bridge, then buffer this request until we
      #  have exited the bridge.
      print("{0} received request from {1}".format(self.index, requester.index))
      
      if self.is_on_bridge:
        print("{0} buffering request from {1}".format(self.index, requester.index))
        self.buffered_requests.append(requester)

      else:
        has_not_requested_access = (self.timestamp is None)
        timestamp_is_newer = (self.timestamp > t)
        has_higher_ID_and_timestamps_equal = (self.index > requester.index and self.timestamp == t)

        print(has_not_requested_access)
        print(timestamp_is_newer)
        print(has_higher_ID_and_timestamps_equal)
        if (has_not_requested_access
            or timestamp_is_newer
            or has_higher_ID_and_timestamps_equal):
          print("{0} sends ack to {1}".format(self.index, requester.index))
	  requester.acknowledge(self)

    
    def leave_bridge(self):
      self.is_on_bridge = False
      while self.buffered_requests:
        v = self.buffered_requests.pop(0)
        v.acknowledge(self)


    def acknowledge(self, other):
      # This car is granted an acknowledgement to its request from the
      #  grantingVehicle
      print("{0} received ack from {1}".format(self.index, other.index))
      self.acknowledgements[other] = True
      if all(self.acknowledgements.values()):
        print("All acks received! Crossing bridge.")
        self.cross_bridge()
   
    
    def cross_bridge(self):
      self.timestamp = None
      self.is_on_bridge = True
      drive_path = get_movement_path(self.sprite.position, self)
      request_bridge_access = CallFunc(self.request_access_to_bridge)
      self.sprite.do(drive_path + request_bridge_access)


    def move(self):
        if self.position >= 1 and self.status != Car_Status.Warning: #If the road has been traveled and not on road 2 or 6
            self.current_road += 1 #Go to the next road
            self.position = 0 #Start over

            if self.current_road % 2 == 0: #Vehicle rotation
                mod = 0
                if self.current_road == 0 or self.current_road == 4:
                    if self.current_road == 4:
                        mod = -1
                    else:
                        mod = -4.2142857
                else:
                    if self.current_road == 2:
                        mod = 1
                    else:
                        mod = 4.2142857
                self.sprite.do(RotateTo(mod*56, 0))
            if self.current_road == 1 or self.current_road == 5:
                mod = 0
                if self.current_road == 1:
                    mod = -1
                else:
                    mod = 1
                self.sprite.do(RotateTo(mod*90, 0))
        else:
            if self.position >= 0.85 and self.status == Car_Status.Warning: #Stop short before bridge, mostly cosmetic
                self.status = Car_Status.Waiting
                self.create_timestamp()
                return
            if self.status == Car_Status.On_Bridge:
                self.position = 0
                self.current_road = 3
                self.sprite.do(RotateTo(0, 0))

        current_road_start_loc = self.road_map[self.current_road][0]
        current_road_end_loc = self.road_map[self.current_road][1]
        road_length = math.sqrt(math.pow((current_road_end_loc[0] - current_road_start_loc[0]), 2) +
                               math.pow((current_road_end_loc[1] - current_road_start_loc[1]), 2))

        self.position += (1.0 / road_length) * (1 + self.speed / 100) #Step size
        self.sprite.do(
            MoveTo(
                    (
                        (current_road_start_loc[0] + ((current_road_end_loc[0] - current_road_start_loc[0]) * self.position)),
                        (current_road_start_loc[1] + ((current_road_end_loc[1] - current_road_start_loc[1]) * self.position))
                    ), 0.6)
        )

        self.label.position = (self.sprite.position[0] + 10, self.sprite.position[1] + 10)

    def check_for_bridge(self):
        if self.status == Car_Status.Waiting:
            print("Vehicle " + str(self.index) + " is waiting at the bridge!")
            #return self.handle_cs()

        if ((self.current_road == 2) or (self.current_road == 6) and
            (self.status != Car_Status.Warning and self.status != Car_Status.Waiting)):
            print("Vehicle " + str(self.index) + " is near the bridge!")
            self.status = Car_Status.Warning
            return True
