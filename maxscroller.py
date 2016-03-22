#!/usr/bin/python
#
#  original code from adafruit, see below copyrights
#  hacked version for bioreactor one
#
#--------------------------------------------------------------------------------------------
# -- 031616 -- converting temp to fahrenhight, and logging
# -- 031816 -- adding in the led libraries to do a simple test, hopefully will add scrolling display
# -- 031816 -- well, attempt at creating a font library for the 8x8 screen,
#              since they aint one.
# -- 031916 -- (b) reverse the current characters
#           -- (g) open the log, and get the temp in f and humidity in h, with dec
#			--	   then build the logic to display the right character.
#           -- (s) implement the rest of the characters
# -- 032116 -- just received the max7219, branching to max2719_scroller,
#			-- attempting to intgrate the new display and add time
#			--	(s) add feature for weather, stocks, and headlines.
#			-- also removed the adafruit webIDE, checking it didn't catasrophically
#			-- fuck up anything else with it.. also upgrading and updating... fingers crossed...
#---------------------------------------------------------------------------------------------------
#
#                .=-.-.  _,.---._                ,---.
#      _..---.  /==/_ /,-.' , -  `.    _.-.    .--.'  \        _..---.
#    .' .'.-. \|==|, |/==/_,  ,  - \ .-,.'|    \==\-/\ \     .' .'.-. \
#   /==/- '=' /|==|  |==|   .=.     |==|, |    /==/-|_\ |   /==/- '=' /
#   |==|-,   ' |==|- |==|_ : ;=:  - |==|- |    \==\,   - \  |==|-,   '
#   |==|  .=. \|==| ,|==| , '='     |==|, |    /==/ -   ,|  |==|  .=. \
#   /==/- '=' ,|==|- |\==\ -    ,_ /|==|- `-._/==/-  /\ - \ /==/- '=' ,|
#  |==|   -   //==/. / '.='. -   .' /==/ - , ,|==\ _.\=\.-'|==|   -   /
#  `-._`.___,' `--`-`    `--`--''   `--`-----' `--`        `-._`.___,'
#      _,.---._    .-._           ,----.
#    ,-.' , -  `. /==/ \  .-._ ,-.--` , \
#   /==/_,  ,  - \|==|, \/ /, /==|-  _.-`
#  |==|   .=.     |==|-  \|  ||==|   `.-.
#  |==|_ : ;=:  - |==| ,  | -/==/_ ,    /
#  |==| , '='     |==| -   _ |==|    .-'
#   \==\ -    ,_ /|==|  /\ , |==|_  ,`-._
#    '.='. -   .' /==/, | |- /==/ ,     /
#      `--`--''   `--`./  `--`--`-----``
#
#          ,--.--------.         ,--.--------.         ,--.--------.
#         /==/,  -   , -\       /==/,  -   , -\       /==/,  -   , -\
#         \==\.-.  - ,-./       \==\.-.  - ,-./       \==\.-.  - ,-./
#          `--`--------`         `--`--------`         `--`--------`
#
#                 ,----.                       ,---.--.          ,-.--, ,---.--.
#     _.-.     ,-.--` , \  _,..---._          /  -_ \==\.--.-.  /=/, .'/  -_ \==\
#   .-,.'|    |==|-  _.-`/==/,   -  \         |` / \/==/\==\ -\/=/- /  |` / \/==/
#  |==|, |    |==|   `.-.|==|   _   _\         \ \ /==/  \==\ `-' ,/    \ \ /==/
#  |==|- |   /==/_ ,    /|==|  .=.   |         /  \==/    |==|,  - |    /  \==/
#  |==|, |   |==|    .-' |==|,|   | -|        /. / \==\  /==/   ,   \  /. / \==\
#  |==|- `-._|==|_  ,`-._|==|  '='   /       | _ \_/\==\/==/, .--, - \| _ \_/\==\
#  /==/ - , ,/==/ ,     /|==|-,   _`/        \ . -  /==/\==\- \/=/ , /\ . -  /==/
#  `--`-----'`--`-----`` `-.`.____.'          '----`--`  `--`-'  `--`  '----`--`
#
#--------------------------------------------------------------------------------

# Copyleft (c) 2016 Alchemy Computing
# Copyright (c) 2014 Adafruit Industries
# Hacker: Justin Knox

# legal shit---------------------------------------------------------------------

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# end of legal shit---------------------------------------------------------------

#---------------------------------------------------
#  .__                              __
#  |__| _____ ______   ____________/  |_  ______
#  |  |/     \\____ \ /  _ \_  __ \   __\/  ___/
#  |  |  Y Y  \  |_> >  <_> )  | \/|  |  \___ \
#  |__|__|_|  /   __/ \____/|__|   |__| /____  >
#           \/|__|                           \/
#
#---------------------------------------------------

import time
import datetime
import max7219.led as led
import time

from max7219.font import proportional, SINCLAIR_FONT, TINY_FONT, CP437_FONT
from random import randrange
from collections import deque



#----------------------------------------------------
#                 .__
#    _____ _____  |__| ____
#   /     \\__  \ |  |/    \
#  |  Y Y  \/ __ \|  |   |  \
#  |__|_|  (____  /__|___|  /
#        \/     \/        \/
#----------------------------------------------------

# ===========================================================================
# 8x8 Pixel Example
#
# ===========================================================================

toggle = True
sleepCount = 0

print "-----=-=-=-------=-  bioreactor-one - montior-one -=---------=-=-=--------"
print "  .... testing .... pixels ... LEDS .................... "
print "-------=---------=---------------------------------=-----------=----------"
print "Press CTRL+Z to exit"
print "--------------------------------------------------------------------------"


device = led.matrix(cascaded=1)

device.orientation(180)

#device.show_message("-----=-=-=-------=-  bioreactor-one - montior-one -=---------=-=-=--------\
#																								   \
#						.... testing .... pixels ... LEDS ....................					   \
#						", font=proportional(CP437_FONT))
#
# open the log for reading values
#----------------------------------------------------------------------------------
print "-----=-=-=-------=-  bioreactor-one - montior-one -=---------=-=-=--------"
tempValFlog = open("/home/pi/curr_F.log", "r");
print "Opening log...  .", tempValFlog.name, " ...in..", tempValFlog.mode, "..access mode."
tempValHlog = open("/home/pi/curr_H.log", "r");
print "Opening log...  .", tempValHlog.name, " ...in..", tempValHlog.mode, "..access mode."
print "-------=---------=---------------------------------=-----------=----------"
print " press CTL-Z to exit "
print "--------------------------------------------------------------------------"


prevFloatFval = 0
prevFloatHval = 0


scrollon = True

#device.show_message(" Welcome to BioLabOne - AlchemyComputing ")



while(scrollon):

	print "-----=-=-=-------=-  bioreactor-one - montior-one -=---------=-=-=--------"
	tempValFlog = open("/home/pi/curr_F.log", "r");
	print "Opening log...  .", tempValFlog.name, " ...in..", tempValFlog.mode, "..access mode."
	tempValHlog = open("/home/pi/curr_H.log", "r");
	print "Opening log...  .", tempValHlog.name, " ...in..", tempValHlog.mode, "..access mode."


	#----------------------------------------------------------------------------------
	# 032116 -- new strategy is to open the log, check for a new value,
	#		 -- if there's no new value, close the log, and wait half a second
	#		 -- if there is a new value, display the new value, and close the log!
	#----------------------------------------------------------------------------------
	
	currentF = tempValFlog.read(5)
	currentH = tempValHlog.read(5)
	
	print "Got values..."
	print "....current from log F: ", currentF
	print "....current fom log H: ", currentH
	print "--------------------"

	
	#--------------------------------------------------------
	# closing the log just in case simple_logger.py needs it
	#--------------------------------------------------------
	print "Closing log...", tempValFlog.name
	print "Closing log...", tempValHlog.name
	tempValFlog.close()
	tempValHlog.close()
	print " ", tempValFlog.closed
	print " ", tempValHlog.closed
	print "--------------------------=-=-=-=-=-=------------------------------------------"
	
	
	# 032216 -- converting back in the old code that grabbed the decimal values
	#first we have to isolate the 100's place, in this case 0
	#if the 100's is 0, then we'll display a space
	#then lets grab the 10's, 1's and the decimal portion.
	#also, we gotta typecast the shit out of this cause of pythons implicit typing...
	hundyPlaceFval = int(float(currentF) / 100)
	tensPlaceFval = int(float(currentF) / 10)
	onesPlaceFval = int( float(currentF) - (hundyPlaceFval*100 + tensPlaceFval*10)  )
	decimalPlaceFval = int((float(currentF) - ( hundyPlaceFval + tensPlaceFval + onesPlaceFval )) * 10)
	decimalPlaceFval /= 100
	#lets see what we got
	print 'F hundy', int(hundyPlaceFval)
	print 'F tens', int(tensPlaceFval)
	print 'F ones', int(onesPlaceFval)
	print 'F deci', int(decimalPlaceFval)
	
	#now lets do the Humidity's
	hundyPlaceHval = int(float(currentH) / 100)
	tensPlaceHval = int(float(currentH) / 10)
	onesPlaceHval = int( float(currentH) - (hundyPlaceHval*100 + tensPlaceHval*10)  )
	decimalPlaceHval = int((float(currentH) - ( hundyPlaceHval + tensPlaceHval + onesPlaceHval )) * 10)
	decimalPlaceHval /= 100
	#lets see what we got
	print '\n'
	print 'H hundy', int(hundyPlaceHval)
	print 'H tens', int(tensPlaceHval)
	print 'H ones', int(onesPlaceHval)
	print 'H deci', int(decimalPlaceHval)
	
	floatFval = float(hundyPlaceFval*100 + tensPlaceFval*10 + onesPlaceFval + decimalPlaceFval/10)
	floatHval = float(hundyPlaceHval*100 + tensPlaceHval*10 + onesPlaceHval + decimalPlaceHval/10)
	
	#-------------- always display the values --------------------------------------------
	device.show_message( " F: " )
	device.show_message( str( floatFval ) )
	device.letter(0, 248)
	device.show_message( " H: " )
	device.show_message( str( floatHval ) )
	device.show_message("%")
	device.show_message( time.strftime("%c"))
	
	#------------------------------------------code below only shows when temp changes
	
	
	
	
	#-----------------------------------------------------------------------show fahrenheit
	#device.show_message( "Fahrenheit = "		)
	if( floatFval > (0.1 + prevFloatFval ) ):
		#device.letter(0, 176);time.sleep(1)
		#device.letter(0, 177);time.sleep(1)
		#device.letter(0, 219);time.sleep(1)
		#device.letter(0, 219);time.sleep(1)
		#device.letter(0, 177);time.sleep(1)
		#device.letter(0, 176);time.sleep(1)
		device.show_message( " +F: " )
		device.show_message( str( floatFval ) )
		device.letter(0, 248)
		sleepCount = 0
	if( floatFval < (0.1 - prevFloatFval) ):
		#device.letter(0, 176);time.sleep(1)
		#device.letter(0, 177);time.sleep(1)
		#device.letter(0, 219);time.sleep(1)
		#device.letter(0, 219);time.sleep(1)
		#device.letter(0, 177);time.sleep(1)
		#device.letter(0, 176);time.sleep(1)
		device.show_message( " -F: " )
		device.show_message( str( floatFval ) )
		device.letter(0, 248)
		sleepCount = 0
	if( floatFval == ( prevFloatFval ) ):
		if(sleepCount<6):
			device.show_message( " - - - "	 )
		sleepCount+=1

	#-----------------------------------------------------------------------one by one display
	#if(hundyPlaceFval!=0):
	#	device.show_message( str(hundyPlaceFval	)	)
	#device.show_message( str(tensPlaceFval		)	)
	#device.show_message( str(onesPlaceFval		)	)
	#device.show_message(".")
	#device.show_message( str(decimalPlaceFval	)	)


	#------------------------------------------------------------------------show humidity
	#device.show_message( "Humidity = "			)
	if( floatHval > (0.1 + prevFloatHval) ):
		#device.letter(0, 176);time.sleep(1)
		#device.letter(0, 177);time.sleep(1)
		#device.letter(0, 219);time.sleep(1)
		#device.letter(0, 219);time.sleep(1)
		#device.letter(0, 177);time.sleep(1)
		#device.letter(0, 176);time.sleep(1)
		device.show_message( " +H: " )
		device.show_message( str( floatHval ) )
		device.show_message("%")
		sleepCount = 0

	if( floatHval < (0.1 - prevFloatHval) ):
		#device.letter(0, 176);time.sleep(1)
		#device.letter(0, 177);time.sleep(1)
		#device.letter(0, 219);time.sleep(1)
		#device.letter(0, 219);time.sleep(1)
		#device.letter(0, 177);time.sleep(1)
		#device.letter(0, 176);time.sleep(1)
		device.show_message( " -H: " )
		device.show_message( str( floatHval ) )
		device.show_message("%")
		sleepCount = 0

	if( floatHval == ( prevFloatHval  ) ):
		if(sleepCount<4):
			device.show_message( "- - - " )
		sleepCount+=1


	#------------------------------------------------------------------------go to sleep
	if(sleepCount > 3):
		sleepCount-=1
		print "Sleeping ... ", sleepCount
		time.sleep(3)
			
	#------------------------------------------------------------------------single message method
	#-----------------------------------------------------------------------one by one display
	#if(hundyPlaceHval!=0):
	#	device.show_message( str(hundyPlaceHval	)	)
	#device.show_message( str(tensPlaceHval		)	)
	#device.show_message( str(onesPlaceHval		)	)
	#device.show_message(".")
	#device.show_message( str(decimalPlaceHval	)	)

	prevFloatFval = floatFval
	prevFloatHval = floatHval

	#time.sleep(3)

	#device.show_message( "Current Time: ")
	#device.show_message( time.strftime("%c"))

	#tempRSSfeed = open("/home/pi/feeds/feeds.db", "r")
	#feedData = tempRSSfeed.read(end)
	#device.show_message( feedData)









