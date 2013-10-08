#!/usr/bin/python
from emulation import Emulation
from time import sleep
import thread

emulate = Emulation()

a = 1

emulate.cur_lat = 52.3323
emulate.cur_lon = -4.73223
emulate.brng = 212
emulate.sog = 8.0
emulate.print_nmea = True
thread.start_new_thread(emulate.run_gps, ())


while True:
	a = a + 1

	if a == 6:
		emulate.brng = 90
		print "changing course, new brng is " + str(emulate.brng)
	elif a == 12:
		emulate.brng = 270
		print "changing course, new brng is " + str(emulate.brng)
	elif a == 20:
		emulate.brng = 212
		print "changing course, new brng is " + str(emulate.brng)
		a == 0
	
	sleep(5)


