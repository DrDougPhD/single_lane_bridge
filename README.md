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
