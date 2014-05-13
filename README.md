Single-Lane Bridge Problem
==========================

Two islands, A and B, need a bridge between them to allow inter-island commerce. However, the politicians are stupid, and by choosing the engineering firm with the lowest bid, the resulting bridge was built with one lane only so as to reduce costs. Through their boundless stupidity, the politicians chose not to redo the bridge but rather try to make it work by enabling a ticket system to enable cars to cross one at a time.


Decentralized Ticket System
---------------------------

The cost of having a centralized ticketing system was just a little too much for the island's politicians, so they opted to implement a much cheaper decentralized system in which the ticket was simply passed from one driver to another. It only costs the value of the creating the ticket, which was implemented on a used napkin. No rules were put in place for sharing the tickets, but with the people of the islands being rational and fair, they all agreed upon a protocol based on the [Ricart & Agrawalas mutual exclusion algorithm](http://en.wikipedia.org/wiki/Ricart%E2%80%93Agrawala_algorithm). The rules and assumptions are:

1. At most one person on the bridge at any given time
2. No person can be indefinitely prevented from crossing the bridge (no live-lock)
3. Assume all vehicular clocks are synchronized


Redesigned Ticket System
------------------------

By far, the people of the islands are more intelligent than their politicians. They observed that it is silly to have a maximum of one person on the bridge at any time. Multiple people traveling in the same direction can cross the bridge. However, by allowing this, someone on the other side of the bridge could be indefinitely prevented from using the bridge. Thus, the people agreed upon a new ticket sharing protocol where:

1. Many people may be on the bridge at one time given that all bridge-goers are traveling in the same direction (no dead-lock)
2. No person can be indefinitely prevented from crossing the bridge (no live-lock)
3. Assume all vehicular clocks are synchronized

Installation
============

This program requires Python 2.6+ or Python 3.3+ for the language. In addition, it requires the libraries pyglet and cocos2d.


Running
=======

The driver.py script is responsible for starting the GUI. To execute this program, you must call driver.py with a number of command-line parameters:

    $ python driver.py BRIDGE_CROSSING_MODE [speed0 [speed1 [...]]]

  BRIDGE_CROSSING_MODE can be one of the following:
    0 -- Single vehicle crossing at a time
    1 -- Multiple vehicle crossing if vehicles are traveling in
          same direction and are traveling at the same or lower
          speed of the first vehicle.

  speed0-9 indicates the custom initial speed of the vehicles you wish to 
   add.
   You have three options to choose from regarding the custom speed
   parameters:

   1.  If you specify no speed parameters, then five vehicles will be
       instantiated with speeds randomly chosen from 50, 100, 150, 250,
       and 400.
   2.  If you specify one speed parameter, then five vehicles will be
       instantiated with the speed you specified.
   3.  By specifying more than 2 speeds, then the number of speed parameters
       that you supply will correspond to the number of vehicles instantiated.
       Each speed will then be assigned to the appropriate vehicle (speed0 to
       vehicle 0, speed1 to vehicle 1, etc).


Keyboard Controls
------------------------
F1 = Add new vehicle (only before starting simulation)
Numpad + or - = Change speed modifier to positive or negative
Numpad 0 to 9 = Change speed of vehicle 1 or 2 or, etc. (After a speed modifier is chosen)
Enter = Start simulation
ESC   = Stop simulation and exit program


Changing speed during simulation
--------------------------------

Due to the complexity of the underlying gaming framework, Cocos2D, it is
 difficult to allow the speeds to be immediately changed while vehicles are in
 motion. If you change the speed of a vehicle, then this speed will not alter
 the traveling speed of the vehicle until it enters the bridge.

