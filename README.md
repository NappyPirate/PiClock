PiClock
=======

this project is designed to be run on a raspberry pi and
will display a 12 hour clock on a 4 digit 7 segment display
with 12 pins that are properly connected to the GPIO pins
(specific 4 digit display id is sma420564)

the BCM pins on the raspberry pi should be connected to the display like so:

GPIO  | display pin
7    ->	   d1
8    ->	   d2
3    -> 	 d3
2    -> 	 d4
17   ->    a
18   ->    b
27   ->    c
22   ->    d
23   ->    e
24   ->    f
25   ->    g
4    ->    p
