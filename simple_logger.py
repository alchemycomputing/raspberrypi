#!/usr/bin/python
#
#  original code from adafruit, see below copyrights
#  hacked version for bioreactor one
#
#---------------------------------------------------------------
# -- 031616 -- converting temp to fahrenhight, and logging
# -- 031816 -- adding in the led libraries to do a simple test, hopefully will add scrolling display
#--------------------------------------------------------------------------------
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
#     ,-,--.   .=-.-.       ___              _,.---._         _,---.
#   ,-.'-  _\ /==/_ /.-._ .'=.'\   _.-.    ,-.' , -  `.   _.='.'-,  \
#  /==/_ ,_.'|==|, |/==/ \|==|  |.-,.'|   /==/_,  ,  - \ /==.'-     /
#  \==\  \   |==|  ||==|,|  / - |==|, |  |==|   .=.     /==/ -   .-'
#   \==\ -\  |==|- ||==|  \/  , |==|- |  |==|_ : ;=:  - |==|_   /_,-.
#   _\==\ ,\ |==| ,||==|- ,   _ |==|, |  |==| , '='     |==|  , \_.' )
#  /==/\/ _ ||==|- ||==| _ /\   |==|- `-._\==\ -    ,_ /\==\-  ,    (
#  \==\ - , //==/. //==/  / / , /==/ - , ,/'.='. -   .'  /==/ _  ,  /
#   `--`---' `--`-` `--`./  `--``--`-----'   `--`--''    `--`------'
#
#--------------------------------------------------------------------------------

# Copyleft (c) 2016 Alchemy Computing
# Copyright (c) 2014 Adafruit Industries
# Hacker: Justin Knox
# Author: Tony DiCola

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

import Adafruit_DHT
from datetime import datetime
# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.DHT11

# Example using a Beaglebone Black with DHT sensor
# connected to pin P8_11.
#pin = 'P8_11'

# Example using a Raspberry Pi with DHT sensor
# connected to GPIO23.
pin = 4




#----------------------------------------------------
#                 .__
#    _____ _____  |__| ____
#   /     \\__  \ |  |/    \
#  |  Y Y  \/ __ \|  |   |  \
#  |__|_|  (____  /__|___|  /
#        \/     \/        \/
#----------------------------------------------------



#------------------------------------------------------------------------------
# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
#-------------------------------------------------------------------------------
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)


# setup the string for the current time, since python's 
# "implicit variable" types aren't really all that "implicit" 
currentTime = datetime.now()


#-----------------------------------------------
#open the log for updating values
#-----------------------------------------------
templog = open("bioreactor-1_templog.log", "a+");
print "-----=-=-=-------=-  bioreactor-one - montior-one -=---------=-=-=--------"
print "Opening log...  .", templog.name, " ...in..", templog.mode, "..access mode."
tempValFlog = open("bioreactor-1_templogValF.log", "a+");
print "Opening log...  .", tempValFlog.name, " ...in..", tempValFlog.mode, "..access mode."
tempValHlog = open("bioreactor-1_templogValH.log", "a+");
print "Opening log...  .", tempValHlog.name, " ...in..", tempValHlog.mode, "..access mode."
print "-------=---------=---------------------------------=-----------=----------"
print " press x to exit "
print "--------------------------------------------------------------------------"



# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
#-------------------------------------------------------------------------
# wrap this all up in a loop, gonna test for 24 hr.s
# 031616 - changed from loop to running this script in the crontab,
#        - seems to be much more efficient that way, the led scroll code
#        - can then pull the data from this log as well as the web module
#--------------------------------------------------------------------------

#while: True
if humidity is not None and temperature is not None:
	# celcius
	print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
	# fahrenheight
	print 'Temp={0:0.1f}*F  Humidity={1:0.1f}%'.format( (temperature*9)/5+32, humidity )
	#write it to the log file as well, 
	# geez, we have to typecast the string too, oye... 
	templog.write( str(currentTime) )
	templog.write(': Temp={0:0.1f}*F  Humidity={1:0.1f}%\n'.format( (temperature*9)/5+32, humidity) )
    	tempValFlog.write('{0:0.1f}\n'.format( (temperature*9)/5+32) )
	tempValHlog.write( str(humidity) + '\n' )

else:
	print 'Failed to get reading. Try again!'
#		break
#----------------------------------------------------
print "Closing log...", templog.name
print "Closing log...", tempValFlog.name
print "Closing log...", tempValHlog.name
templog.close()
tempValFlog.close()
tempValHlog.close()
print " ", templog.closed
print " ", tempValFlog.closed
print " ", tempValHlog.closed
