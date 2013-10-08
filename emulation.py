#!/usr/bin/python
from random import randint
from math import atan2, sin, cos, degrees as deg, radians as rad, asin, pi
import time, datetime

Copyright (c) 2013 Will Smith - All Rights Reserved

class Emulation:

	ER = 6371
	cur_lat = None			#Current Latitude
	cur_lon = None			#Current Longitude
	sog = 2.537				#Speed Over Ground (in m/s)
	brng = None				#Current Bearing
	sats = 5 				#Current Satilites being used for the fix
	gps_fix = True			#Do We have a GPS Fix?
	last_update = 1 		#Time since last GPS update (Seconds)
	N_S = "N"				#North or South?
	E_W = "W"				#East or West?
	gprmc_nmea = None		#The Current NMEA GGA String
	print_nmea = False		#Print the NMEA String on update?
	gps_update_time = 0.2 	#How often do we update the GPS (in seconds)
	true_wind = 45			#Where is the wind?
	round_dp = 7 			#DP to round Lat/Lon to


	def __init__(self):
		pass


	"""
		run_gps: 	runs the gps emulator updating the gps info based on the speed over ground (sog) value set and the current bearing that the
					simulator has been instructed to use.
	"""
	def run_gps(self):

		try:
			while  True:
				#Randomize the number of satilites in view
				self.randomize_sat()
			
				#Randomize GPS fix loss.		
				self.randomize_gps_loss()
			
				#Calculate the actual speed to update the gps info and then calculate and store it.
				actual_sog = self.sog * self.gps_update_time
				latlon = self.calculate_int_waypoint(self.cur_lat, self.cur_lon, actual_sog, self.brng)
				self.cur_lat = latlon[0]
				self.cur_lon = latlon[1]

				#Which side of the equator are we?
				if self.cur_lat < 0:
					N_S = "S"	#Latitude is negative, we're south of the equator.
				else:
					N_S = "N"	#Latitude is positve, we're north of the equator.

				#Which Hemisphere are we in?
				if self.cur_lon < 0:
					E_W = "W"	#Longitude is negative, we're in the west.
				else:
					E_W = "E"	#Longitiude is positive, we're in the east.

				self.build_gprmc_nmea()

				#If NMEA printing is enabled, then print the string. 
				if self.print_nmea == True:
					print self.gprmc_nmea
				
				#Sleep the loop until the next desired update.
				time.sleep(self.gps_update_time)

		except Exception:
			import traceback
			print traceback.format_exc()
		

	"""
		randomize_sat: 	Randomises the number of satilites 'in use' to be returned in the NMEA string
						if a number divisible by 9 is retuned then the satilite seed is set as the 'new'
						number of satilites in view, if not the number is left unchanged.
	"""
	def randomize_sat(self):
		seed = randint(0,256)
		sat_seed = randint(3,12)
		
		if seed % 9 == 0:
			self.sats = sat_seed
		else:
			self.sats = self.sats

	"""
		randomize_gps_loss:	Randomises total GPS signal loss, there is a 1 in 250 chance that the next message will be reported as dropped,
							you can change this by altering the upper seed/modulus value if needs be.  If a number divisible by 128 is returned 
							then no lat/lon, gps fix info or other satilite related GPS info will be returned in the NMEA string.
	"""
	def randomize_gps_loss(self):
		seed = randint(0,1024)

		if self.gps_fix == True:
			if seed % 3 == 0:
				self.last_update = self.last_update + self.gps_update_time
		elif seed % 128 == 0:
			self.gps_fix = False
			self.sats = 0
			self.last_update = self.last_update + self.gps_update_time
		else:
			self.gps_fix = True
			self.last_update = self.gps_update_time


	"""
		calculate_int_waypoint: Calculates new Lat/Lon depending heading and interpolated speed from the provided information. 

			@dec_lat: Latitude in Degrees.
			@dec_lon: Longitude in Degrees.
			@m_distance: Distance in Meters.
			@dec_brng: Bearing in Degrees.

			returns: A tuple containing lattiude and longitude expressed in degrees in the format (lat, lon).

	"""
	def calculate_int_waypoint(self, dec_lat, dec_lon, m_dist, dec_brng):
		lat = rad(dec_lat)
		lon = rad(dec_lon)
		brng = rad(dec_brng)
		dist = m_dist/1000
	
		new_lat = asin(sin(lat)*cos(dist/self.ER) + cos(lat)*sin(dist/self.ER)*cos(brng))
		new_lon = lon + atan2(sin(brng)*sin(dist/self.ER)*cos(lat),cos(dist/self.ER) - sin(lat)*sin(new_lat))
		norm_new_lon = (new_lon + (3*pi)) % (2*pi) - pi
	
		rnd_lat = deg(new_lat)
		rnd_lon = deg(norm_new_lon)
	
		new_latlon = (rnd_lat, rnd_lon);
	
		return new_latlon

	"""
		build_gprmc_nmea: builds a GPRMC NMEA string based on the current simulated GPS data.
	"""
	def build_gprmc_nmea(self):
		ts = datetime.datetime.fromtimestamp(time.time()).strftime('%H%M%S.%f')
		ds = datetime.datetime.fromtimestamp(time.time()).strftime('%d%m%Y')

		if self.gps_fix == True:
			self.gprmc_nmea = "$GPRMC," + str(ts) + "," + "A," + str(round(self.cur_lat,self.round_dp)) + "," + self.N_S + "," + str(round(self.cur_lon,self.round_dp)) + "," + self.E_W + "," + str(self.sog*1.9438) + "," + str(self.brng) + "," + str(ds) + ",004.2,W*70"
		else:
			self.gprmc_nmea = "$GPRMC, NOFIX"

		return self.gprmc_nmea
         



	
	#def randomise_wind(self, cur_wind, seed):





