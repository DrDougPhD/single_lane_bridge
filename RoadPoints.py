# RoadPoints.py
#  Specify the vehicles that exist on the map between the two cities.
#
# Written by Madeline Cameron and Doug McGeehan
# CS 384 - Distributed Operating Systems
# Spring 2014

class RoadPoints:
  SW = 100, 100
  NW = 100, 400
  SE = 500, 100
  NE = 500, 400

  # Intersections of the road with the bridge.
  W = 200, 250
  E = 400, 250

  # This list is used to draw the roads, showing which vertices
  # are connected to each other.
  ROADMAP = [
    [W, NW],
    [NW, SW],
    [SW, W],
    [W, E],
    [E, SE],
    [SE, NE],
    [NE, E],
  ]

  # This list is used to randomly select one point for initialization.
  POINTS = [SW, NW, SE, NE, W, E]
