#Vehicle.py
#
#Written by Madeline Cameron and Doug McGeehan
#CS 384 - Distributed Operating Systems
#Spring 2014

import random, cocos, time, math, threading
from cocos.actions import MoveTo, RotateTo
from UI import RoadPoints
from cocos.actions import CallFunc
import math
from BridgeMode import BridgeMode

def duration(src, dst, speed):
  x1, y1 = src
  x2, y2 = dst
  d = math.hypot(x2 - x1, y2 - y1)
  return d/float(speed)


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


def getVehicleClassByMode(mode):
  if mode == BridgeMode.One_at_a_Time:
    print("Bridge crossing mode: only one vehicle will have access at a time")
    return VehicleOneAtATime

  if mode == BridgeMode.One_direction:
    print("Bridge crossing mode: all vehicles in one direction will have access")
    return VehicleOneDirection


class VehicleOneAtATime:
    def __init__(self, index, speed):
        print("Initializing vehicle {0}...".format(index))
        
        # "Bridge" is road 3 and no one can start there
        random_road = random.choice([0, 1, 2, 4, 5, 6])
        self.buffered_requests = []
        self.is_on_bridge = False
        self.acknowledgements = {}
        self.other_vehicles = []
        self.timestamp = None

        self.current_road = random_road
        self.index = index
        self.speed = random.choice([100, 200, 150, 60, 50]) #speed
        self.position = 0
        self.label = None
        self.sprite = cocos.sprite.Sprite(
          'car2.png',
          scale=0.10,
          color=[random.randrange(0, 255) for i in range(3)]
        ) #Pick a random color
        self.sprite.position = RoadPoints.ROADMAP[self.current_road][0]
        print("Vehicle {0} initialized!".format(index))


    def set_other_vehicles(self, other_vehicles):
      # By referencing the original list, any modification to it will
      #  immediately be reflected in the local list. That's just how
      #  Python lists work.
      self.other_vehicles = other_vehicles


    def begin(self):
      print(self.other_vehicles)
      drive_path = get_town_travel_path(RoadPoints.ROADMAP[self.current_road][0], self.speed)
      request_bridge_access = CallFunc(self.request_access_to_bridge)
      self.sprite.do(drive_path + request_bridge_access) 


    def __repr__(self):
      return str(self)


    def __str__(self):
      return "{0}".format(self.index)


    def request_access_to_bridge(self):
      # Record the time and reset the acknowledgement tracker.
      now = time.time()
      self.timestamp = now
      print("{0} is requesting bridge access".format(self.index))
      self.acknowledgements = {v:False for v in self.other_vehicles if v.index != self.index}

      # As per Ricart & Agrawala's algorithm, broadcast a timestamped request
      # to all other vehicles.
      for c in self.other_vehicles:
        if (c.index != self.index):
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
        # This car is not on the bridge. However, it could still have a
        #  request that is newer than the received request.
        timestamp_is_newer = (self.timestamp > t)
        has_higher_ID_and_timestamps_equal = (
          self.index > requester.index and
          self.timestamp == t
        )
        # If there is no pending request, or if the pending request is
        #  newer than the sent one, or if they are equal and the sender
        #  has a lower ID, then grant them their acknowledgment.
        if (self.timestamp is None or
            timestamp_is_newer or
            has_higher_ID_and_timestamps_equal):
          print("{0} sends ack to {1}".format(self.index, requester.index))
          requester.acknowledge(self)

        else:
          print("{0} buffering request from {1}".format(self.index, requester.index))
          self.buffered_requests.append(requester)


    def leave_bridge(self):
      print("{0} releases token to {1} pending requests".format(
        self.index,
        len(self.buffered_requests)
      ))
      self.is_on_bridge = False
      while self.buffered_requests:
        v = self.buffered_requests.pop(0)
        v.acknowledge(self)


    def acknowledge(self, other):
      # This car is granted an acknowledgement to its request from the
      #  grantingVehicle
      print("{0} received ack from {1}".format(self.index, other.index))
      self.acknowledgements[other] = True
      for v in self.acknowledgements:
        print("{0} checking for acknowledgement for {1}: {2}".format(
          self.index,
          v.index,
          self.acknowledgements[v]
        ))

      if all(self.acknowledgements.values()):
        print("All acks received! Crossing bridge.")
        self.cross_bridge()


    def cross_bridge(self):
      self.timestamp = None
      self.is_on_bridge = True
      drive_path = get_movement_path(self.sprite.position, self)
      request_bridge_access = CallFunc(self.request_access_to_bridge)
      self.sprite.do(drive_path + request_bridge_access)


class VehicleOneDirection:
    def __init__(self, index, speed):
        print("Initializing vehicle {0}...".format(index))
        
        # "Bridge" is road 3 and no one can start there
        random_road = random.choice([0, 1, 2, 4, 5, 6])
        self.buffered_requests = []
        self.is_on_bridge = False
        self.acknowledgements = {}
        self.other_vehicles = []
        self.timestamp = None
        self.current_road = random_road

        # Upon initialization, self.bridge_entry_point must be set to the
        #  bridge entry point that is immediately behind the vehicle. This
        #  is required so that this value can be simply flipped when the
        #  vehicle approaches the bridge again.
        current_point = RoadPoints.ROADMAP[self.current_road][1]
        if any(current_point == P for P in [RoadPoints.W, RoadPoints.SW, RoadPoints.NW]):
          self.bridge_entry_point = RoadPoints.E

        else:
          self.bridge_entry_point = RoadPoints.W

        print("self.bridge_entry_point := {0}".format(self.bridge_entry_point))

        self.index = index
        self.speed = random.choice([100, 200, 150, 60, 50]) #speed
        self.position = 0
        self.label = None
        self.sprite = cocos.sprite.Sprite(
          'car2.png',
          scale=0.10,
          color=[random.randrange(0, 255) for i in range(3)]
        ) #Pick a random color
        self.sprite.position = RoadPoints.ROADMAP[self.current_road][0]
        print("Vehicle {0} initialized!".format(index))


    def set_other_vehicles(self, other_vehicles):
      # By referencing the original list, any modification to it will
      #  immediately be reflected in the local list. That's just how
      #  Python lists work.
      self.other_vehicles = other_vehicles


    def begin(self):
      print(self.other_vehicles)
      drive_path = get_town_travel_path(RoadPoints.ROADMAP[self.current_road][0], self.speed)
      request_bridge_access = CallFunc(self.request_access_to_bridge)
      self.sprite.do(drive_path + request_bridge_access) 


    def __repr__(self):
      return str(self)


    def __str__(self):
      return "{0}".format(self.index)


    def request_access_to_bridge(self):
      # Record the time and reset the acknowledgement tracker.
      now = time.time()
      self.timestamp = now
      print("{0} is requesting bridge access".format(self.index))
      self.acknowledgements = {v:False for v in self.other_vehicles if v.index != self.index}
      print("{0} bridge entry is {1}".format(self, self.bridge_entry_point))
      self.flip_entry_point()
      print("{0} bridge entry is updated to {1}".format(self, self.bridge_entry_point))

      # As per Ricart & Agrawala's algorithm, broadcast a timestamped request
      # to all other vehicles.
      for c in self.other_vehicles:
        if (c.index != self.index):
          print("{0} sent request to {1}".format(self.index, c.index))
          c.request(requester=self, t=now, bridge_entry=self.bridge_entry_point)


    def request(self, requester, t, bridge_entry):
      # As per Ricart & Agrawala's algorithm, the requester has broadcast a
      #  timestamped request to all vehicles. This vehicle has received the
      #  request and checks if it needs access to the bridge. Return an 
      #  acknowledgement if:
      #    1. This vehicle does not need access to the bridge
      #    2. This vehicle's request occurred later than the other vehicle
      # If we are already on the bridge, then buffer this request until we
      #  have exited the bridge.
      # 
      # Requires:
      #  self.bridge_entry_point is the point at which the current vehicle
      #   entered the bridge. This does not change until the vehicle
      #   enters the bridge again from the other side.
      #
      #  self.same_direction_head
      #   self.same_direction_head needs to be set only if bridge access occurs
      #   self.same_direction_head needs to be unset when this vehicle leaves
      #   the bridge.
      print("{0} received request from {1}".format(self.index, requester.index))
      print("{0} came from {1}".format(self, self.bridge_entry_point))
      print("{0} is at {1}".format(requester, bridge_entry))
      if self.bridge_entry_point == bridge_entry or (self.timestamp is None and self.is_on_bridge != True):
              print("{0} will ack {1}".format(self, requester))
              requester.acknowledge(self)
      else:
              print("{0} buffers request from {1}".format(self, requester))
              self.buffered_requests.append(requester)
      """
      if self.is_on_bridge:
        if self.bridge_entry_point == bridge_entry:
          # This vehicle is on the bridge, and the requesting vehicle is
          #  requesting to travel the bridge in the same direction. Thus, this
          #  vehicle should grant access to the bridge.
          requester.same_direction_ack(
            acknowledger=self,
            head=self.same_direction_head
          )
          self.same_direction_tail = requester

        else:
          print("{0} buffering request from {1}".format(self.index, requester.index))
          self.buffered_requests.append(requester)

      else:
        # This car is not on the bridge. However, it could still have a
        #  request that is newer than the received request.
        timestamp_is_newer = (self.timestamp > t)
        has_higher_ID_and_timestamps_equal = (
          self.index > requester.index and
          self.timestamp == t
        )
        # If there is no pending request, or if the pending request is
        #  newer than the sent one, or if they are equal and the sender
        #  has a lower ID, then grant them their acknowledgment.
        if (self.timestamp is None or
            timestamp_is_newer or
            has_higher_ID_and_timestamps_equal):
          print("{0} sends ack to {1}".format(self.index, requester.index))
          requester.acknowledge(self)

        else:
          print("{0} buffering request from {1}".format(self.index, requester.index))
          self.buffered_requests.append(requester)
      """


    def same_direction_ack(acknowledger, head):
      self.same_direction_head = head
      self.same_direction_tail = self
      self.acknowledge(other=acknowledger)


    def leave_bridge(self):
      print("{0} releases token to {1} pending requests".format(
        self.index,
        len(self.buffered_requests)
      ))
      self.is_on_bridge = False
      while self.buffered_requests:
        v = self.buffered_requests.pop(0)
        v.acknowledge(self)


    def acknowledge(self, other):
      # This car is granted an acknowledgement to its request from the
      #  grantingVehicle
      print("{0} received ack from {1}".format(self.index, other.index))
      self.acknowledgements[other] = True
      for v in self.acknowledgements:
        print("{0} checking for acknowledgement for {1}: {2}".format(
          self.index,
          v.index,
          self.acknowledgements[v]
        ))

      if all(self.acknowledgements.values()):
        print("All acks received! Crossing bridge.")
        self.cross_bridge()


    def flip_entry_point(self):
      if self.bridge_entry_point == RoadPoints.W:
        self.bridge_entry_point = RoadPoints.E

      else:
        self.bridge_entry_point = RoadPoints.W


    def cross_bridge(self):
      # Requires:
      #  self.bridge_entry_point should be equal to the bridge entry point
      #    that is on the other side of the bridge (e.g. if we are heading
      #    west, and are at the Eastern entrance, then self.bridge_entry_point
      #    should be equal to RoadPoints.W)
      #self.flip_entry_point()
      self.timestamp = None
      self.is_on_bridge = True
      drive_path = get_movement_path(self.sprite.position, self)
      request_bridge_access = CallFunc(self.request_access_to_bridge)
      self.sprite.do(drive_path + request_bridge_access)
