# Vehicle.py
#
# Written by Madeline Cameron and Doug McGeehan
# CS 384 - Distributed Operating Systems
# Spring 2014

import random
import cocos
import time
import math
from cocos.actions import MoveTo
from cocos.actions import RotateTo
from cocos.actions import CallFunc
from RoadPoints import RoadPoints
from BridgeMode import BridgeMode


# Given two points and the speed at which to travel between these points,
#  return the time required for travel.
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
      CallFunc(vehicle.rotate_E) + \
      MoveTo(RoadPoints.E, duration(starting_point, RoadPoints.E, vehicle.speed)) + \
      CallFunc(vehicle.leave_bridge) + \
      get_town_travel_path(RoadPoints.E, vehicle)
    )

  elif starting_point == RoadPoints.E:
    # Cross the bridge from East to West.
    #  It is assumed the car is currently at RoadPoints.W
    #  E -> W -> SW -> NW -> W
    return (
      CallFunc(vehicle.rotate_W) + \
      MoveTo(RoadPoints.W, duration(starting_point, RoadPoints.W, vehicle.speed)) + \
      CallFunc(vehicle.leave_bridge) + \
      get_town_travel_path(RoadPoints.W, vehicle)
    )


def get_town_travel_path(starting_point, vehicle):
  """When a process is given the token for entry on the bridge, it will
  be permitted to cross the bridge and drive through the town."""

  if starting_point == RoadPoints.E:
    # Travel the Eastern Town.
    #  It is assumed the car is currently at RoadPoints.E
    #  E -> NE -> SE -> E
    return (
      CallFunc(vehicle.rotate_NE) + \
      MoveTo(RoadPoints.NE, duration(RoadPoints.E, RoadPoints.NE, vehicle.speed)) + \
      CallFunc(vehicle.rotate_S) + \
      MoveTo(RoadPoints.SE, duration(RoadPoints.NE, RoadPoints.SE, vehicle.speed)) + \
      CallFunc(vehicle.rotate_NW) + \
      MoveTo(RoadPoints.E, duration(RoadPoints.SE, RoadPoints.E, vehicle.speed))
    )

  elif starting_point == RoadPoints.NE:
    # Travel the Eastern Town.
    #  It is assumed the car is currently at RoadPoints.E
    #  NE -> SE -> E
    return (
      CallFunc(vehicle.rotate_S) + \
      MoveTo(RoadPoints.SE, duration(RoadPoints.NE, RoadPoints.SE, vehicle.speed)) + \
      CallFunc(vehicle.rotate_NW) + \
      MoveTo(RoadPoints.E, duration(RoadPoints.SE, RoadPoints.E, vehicle.speed))
    )

  elif starting_point == RoadPoints.SE:
    # Travel the Eastern Town.
    #  It is assumed the car is currently at RoadPoints.E
    #  SE -> E
    return (
      CallFunc(vehicle.rotate_NW) + \
      MoveTo(RoadPoints.E, duration(RoadPoints.SE, RoadPoints.E, vehicle.speed))
    )

  elif starting_point == RoadPoints.W:
    # Travel the Western Town.
    #  It is assumed the car is currently at RoadPoints.W
    #  W -> SW -> NW -> W
    return (
      CallFunc(vehicle.rotate_SW) + \
      MoveTo(RoadPoints.SW, duration(RoadPoints.W, RoadPoints.SW, vehicle.speed)) + \
      CallFunc(vehicle.rotate_N) + \
      MoveTo(RoadPoints.NW, duration(RoadPoints.SW, RoadPoints.NW, vehicle.speed)) + \
      CallFunc(vehicle.rotate_SE) + \
      MoveTo(RoadPoints.W, duration(RoadPoints.NW, RoadPoints.W, vehicle.speed))
    )

  elif starting_point == RoadPoints.SW:
    # Travel the Western Town.
    #  SW -> NW -> W
    return (
      CallFunc(vehicle.rotate_N) + \
      MoveTo(RoadPoints.NW, duration(RoadPoints.SW, RoadPoints.NW, vehicle.speed)) + \
      CallFunc(vehicle.rotate_SE) + \
      MoveTo(RoadPoints.W, duration(RoadPoints.NW, RoadPoints.W, vehicle.speed))
    )

  elif starting_point == RoadPoints.NW:
    # Travel the Western Town.
    #  NW -> W
    return (
      CallFunc(vehicle.rotate_SE) + \
      MoveTo(RoadPoints.W, duration(RoadPoints.NW, RoadPoints.W, vehicle.speed))
    )


def getVehicleClassByMode(mode):
  if mode == BridgeMode.One_at_a_Time:
    print("Bridge crossing mode: only one vehicle will have access at a time")
    return VehicleOneAtATime

  if mode == BridgeMode.One_direction:
    print("Bridge crossing mode: all vehicles in one direction will have access")
    return VehicleOneDirection


# Abstract base class
class Vehicle(cocos.layer.Layer):

  # Static ID so that each vehicle has a unique ID.
  ID = 0

  def __init__(self, speed):
    super(Vehicle, self).__init__()
    self.index = Vehicle.ID
    print("Initializing vehicle {0}...".format(self.index))

    Vehicle.ID += 1
    self.speed = speed

    self.is_on_bridge = False
    self.timestamp = None
    self.buffered_requests = []
    self.acknowledgements = {}
    self.other_vehicles = []

    self.initial_point = random.choice(RoadPoints.POINTS)
    self.position = self.initial_point

    self.sprite = cocos.sprite.Sprite(
      'car2.png',
      scale=0.10,
      color=[random.randrange(0, 255) for i in range(3)]
    )
    # Create the car sprite.
    self.add(self.sprite)

    if self.initial_point == RoadPoints.SW: 
        self.sprite.do(RotateTo(-90, 0))
    if self.initial_point == RoadPoints.NE: 
        self.sprite.do(RotateTo(90, 0))
    if self.initial_point == RoadPoints.NW: 
        self.sprite.do(RotateTo(56, 0))
    if self.initial_point == RoadPoints.SE: 
        self.sprite.do(RotateTo(236, 0))
    if self.initial_point == RoadPoints.W:
        self.sprite.do(RotateTo(-236, 0))
    if self.initial_point == RoadPoints.E:
        self.sprite.do(RotateTo(-56, 0))

    # Create the car label that will travel with the car.
    self.add(cocos.text.Label(
      str(self.index),
      position=(0, 10),
      color=(255, 255, 255, 255)
    ))

    print("Vehicle {0} initialized!".format(self))


  def __repr__(self):
    # Create a string representation of this vehicle for standard output.
    return str(self)


  def __str__(self):
    # Create a string representation of this vehicle for standard output.
    return "{0}".format(self.index)


  def set_other_vehicles(self, other_vehicles):
    # By referencing the original list, any modification to it will
    #  immediately be reflected in the local list. That's just how
    #  Python lists work.
    self.other_vehicles = other_vehicles


  def begin(self):
    # Upon initialization, this function is called to set the
    #  vehicles motion based on where it was initialized.
    drive_path = get_town_travel_path(
      self.initial_point,
      self
    )
    request_bridge_access = CallFunc(self.request_access_to_bridge)
    self.do(drive_path + request_bridge_access)


  def request_access_to_bridge(self):
    # Precondition: this vehicle is at one of the entrances to the bridge.
    #  This vehicle will call this function when it requests access to the
    #  bridge, following the Ricart & Agrawala algorithm

    # Record the time and reset the acknowledgement tracker.
    self.timestamp = time.time()
    print("{0} is requesting bridge access".format(self.index))
    self.acknowledgements = {
      v:False for v in self.other_vehicles if v.index != self.index
    }

    # As per Ricart & Agrawala's algorithm, broadcast a timestamped request
    # to all other vehicles.
    for c in self.other_vehicles:
      if (c.index != self.index):
        print("{0} sent request to {1}".format(self.index, c.index))
        c.request(self)


  def leave_bridge(self):
    # This function is called immediately once the vehicle leaves the bridge
    #  by crossing one of the exit points.
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
    #  grantingVehicle. As per the Ricart & Agrawala algorithm, it must
    #  check to see if all acknowledgements have been received.
    #
    # If all acknowledgements have been received, then it is granted
    #  access to the bridge.
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
    # Precondition: no vehicle is on the bridge that will cause a fatal head-on
    #  collision (derived classes of this Vehicle base class may permit
    #  multiple vehicles to access the bridge based on non-conflicting
    #  criteria, such as traveling the same direction).
    #
    #  This vehicle may now drive across the bridge, travel through the town
    #  and then re-request access to the bridge once it has arrived at the
    #  entrance again.
    self.timestamp = None
    self.is_on_bridge = True
    drive_path = get_movement_path(self.position, self)
    request_bridge_access = CallFunc(self.request_access_to_bridge)
    self.do(drive_path + request_bridge_access)


  def rotate(self, angle):
    # Rotate the vehicle to the angle specified.
    self.sprite.do(RotateTo(angle, 0))


  def rotate_SW(self):
    # This should be called if the vehicle is exiting the bridge from
    #  the western point.
    self.rotate(-236)


  def rotate_N(self):
    # This should be called if the vehicle is at the SW point.
    self.rotate(-90)


  def rotate_SE(self):
    # This should be called if the vehicle is at the NW point.
    self.rotate(56)


  def rotate_E(self):
    # This should be called if the vehicle is entering the bridge at the
    #  western entrace.
    self.rotate(0)


  def rotate_NE(self):
    # This should be called if the vehicle is exiting the bridge from the
    #  eastern point.
    self.rotate(-56)


  def rotate_S(self):
    # This should be called if the vehicle is at the NE point.
    self.rotate(90)


  def rotate_NW(self):
    # This should be called if the vehicle is at the SE point.
    self.rotate(236)


  def rotate_W(self):
    # This should be called if the vehicle is entering the bridge at the
    #  eastern entrance.
    self.rotate(180)


class VehicleOneAtATime(Vehicle):
  # This class only permits one vehicle to access the bridge at any time, where
  #  access is granted based on timestamped (and in case of ties, lower ID)
  #  priority.


  def request(self, requester):
    t = requester.timestamp
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
      #
      # If there is no pending request, or if the pending request is
      #  newer than the sent one, or if they are equal and the sender
      #  has a lower ID, then grant them their acknowledgment.
      if (
        # Vehicle has not made a request
        (self.timestamp is None) or
        # This vechile has a newer timestamp, thus lower priority
        (self.timestamp > t) or
        # The timestamps are equal, in which case the car with the smaller
        #  index has higher priority.
        (self.index > requester.index and self.timestamp == t)
      ):
        print("{0} sends ack to {1}".format(self.index, requester.index))
        requester.acknowledge(self)

      else:
        # This vehicle is either on the bridge, or it has higher priority over
        #  bridge access than the requester. The request will be buffered
        #  until this vehicle has crossed the bridge.
        print("{0} buffering request from {1}".format(self.index, requester.index))
        self.buffered_requests.append(requester)


class VehicleOneDirection(Vehicle):
  # This class permits multiple vehicles to travel across the bridge
  #  at a time assuming they are traveling in the same direction. If a vehicle
  #  is already on the bridge, and a request from the other side is made, then
  #  no other vehicles will be granted access until the vehicle from the other
  #  side is granted access. This prevents livelock from occurrying.

  def __init__(self, speed):
    Vehicle.__init__(self, speed)

    # Upon initialization, self.bridge_entry_point must be set to the
    #  bridge entry point that is immediately behind the vehicle. This
    #  is required so that this value can be simply flipped when the
    #  vehicle approaches the bridge again.
    if any(self.initial_point == P for P in [RoadPoints.W, RoadPoints.SW, RoadPoints.NW]):
      self.bridge_entry_point = RoadPoints.E

    else:
      self.bridge_entry_point = RoadPoints.W

    print("self.bridge_entry_point := {0}".format(self.bridge_entry_point))


  def request_access_to_bridge(self):
    # Precondition: this vehicle is at an entrance to the bridge, and its
    #  self.bridge_entry_point is set to the other entrance of the bridge.
    self.flip_entry_point()
    Vehicle.request_access_to_bridge(self)


  def request(self, requester):
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
    t = requester.timestamp
    bridge_entry = requester.bridge_entry_point
    print("{0} received request from {1}".format(self.index, requester.index))
    print("{0} came from {1}".format(self, self.bridge_entry_point))
    print("{0} is at {1}".format(requester, bridge_entry))
    if (self.bridge_entry_point == bridge_entry or
       (self.timestamp is None and self.is_on_bridge != True)
    ):
      print("{0} will ack {1}".format(self, requester))
      requester.acknowledge(self)
    else:
      print("{0} buffers request from {1}".format(self, requester))
      self.buffered_requests.append(requester)


  def flip_entry_point(self):
    if self.bridge_entry_point == RoadPoints.W:
      self.bridge_entry_point = RoadPoints.E

    else:
      self.bridge_entry_point = RoadPoints.W

