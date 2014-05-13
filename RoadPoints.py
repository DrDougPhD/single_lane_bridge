
class RoadPoints:
  SW = 100, 100
  NW = 100, 400
  SE = 500, 100
  NE = 500, 400

  # Intersections of the road with the bridge.
  W = 200, 250
  E = 400, 250

  ROADMAP = [
    [W, NW],
    [NW, SW],
    [SW, W],
    [W, E],
    [E, SE],
    [SE, NE],
    [NE, E],
  ]

  POINTS = [SW, NW, SE, NE, W, E]



