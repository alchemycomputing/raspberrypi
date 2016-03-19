#!/usr/bin/python
#
#  original code from adafruit, see below copyrights
#  hacked version for bioreactor one
#
#---------------------------------------------------------------
# -- 031616 -- converting temp to fahrenhight, and logging
# -- 031816 -- adding in the led libraries to do a simple test, hopefully will add scrolling display
# -- 031816 -- well, attempt at creating a font library for the 8x8 screen,
#              since they aint one.
# -- 031916 -- (b) reverse the current characters
#           -- (g) open the log, and get the temp in f and humidity in h, with dec
#			--	   then build the logic to display the right character.
#           -- (s) implement the rest of the characters
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
from Adafruit_8x8 import ColorEightByEight
from collections import deque


grid = ColorEightByEight(address=0x70)


print "-----=-=-=-------=-  bioreactor-one - montior-one -=---------=-=-=--------"
print "  .... testing .... pixels ... LEDS .................... "
print "-------=---------=---------------------------------=-----------=----------"
print "Press CTRL+Z to exit"
print "--------------------------------------------------------------------------"


iter = 0

#----------------------------------------------------------------------------
# test code from orig library, cycles through each led
#
#----------------------------------------------------------------------------
# Continually update the 8x8 display one pixel at a time
#while(True):
#    iter += 1
#
#    for x in range(0, 8):
#        for y in range(0, 8):
#            grid.setPixel(x, y, iter % 4 )
#           time.sleep(0.015625)
#           print x, ":", y, ":", iter % 4


smileyRow0 = deque([0,0,1,1,1,1,0,0, 0]); smileyRow0.reverse()
smileyRow1 = deque([0,1,0,0,0,0,1,0, 0]); smileyRow1.reverse()
smileyRow2 = deque([1,0,1,0,0,1,0,1, 0]); smileyRow2.reverse()
smileyRow3 = deque([1,0,0,0,0,0,0,1, 0]); smileyRow3.reverse()
smileyRow4 = deque([1,0,1,0,0,1,0,1, 0]); smileyRow4.reverse()
smileyRow5 = deque([1,0,0,1,1,0,0,1, 0]); smileyRow5.reverse()
smileyRow6 = deque([0,1,0,0,0,0,1,0, 0]); smileyRow6.reverse()
smileyRow7 = deque([0,0,1,1,1,1,0,0, 0]); smileyRow7.reverse()

aRow0 = deque([0,0,1,1,1,1,0,0, 0]); aRow0.reverse()
aRow1 = deque([0,1,1,0,0,1,1,0, 0]); aRow1.reverse()
aRow2 = deque([1,1,0,0,0,0,1,1, 0]); aRow2.reverse()
aRow3 = deque([1,1,0,0,0,0,1,1, 0]); aRow3.reverse()
aRow4 = deque([1,1,1,1,1,1,1,1, 0]); aRow4.reverse()
aRow5 = deque([1,1,0,0,0,0,1,1, 0]); aRow5.reverse()
aRow6 = deque([1,1,0,0,0,0,1,1, 0]); aRow6.reverse()
aRow7 = deque([1,1,0,0,0,0,1,1, 0]); aRow7.reverse()

oneRow0 = deque([0,0,0,1,1,0,0,0, 0]); oneRow0.reverse()
oneRow1 = deque([0,0,1,1,1,0,0,0, 0]); oneRow1.reverse()
oneRow2 = deque([0,1,1,1,1,0,0,0, 0]); oneRow2.reverse()
oneRow3 = deque([1,1,0,1,1,0,0,0, 0]); oneRow3.reverse()
oneRow4 = deque([0,0,0,1,1,0,0,0, 0]); oneRow4.reverse()
oneRow5 = deque([0,0,0,1,1,0,0,0, 0]); oneRow5.reverse()
oneRow6 = deque([1,1,1,1,1,1,1,1, 0]); oneRow6.reverse()
oneRow7 = deque([1,1,1,1,1,1,1,1, 0]); oneRow7.reverse()

twoRow0 = deque([0,0,1,1,1,1,0,0, 0]); twoRow0.reverse()
twoRow1 = deque([0,1,1,1,1,1,1,0, 0]); twoRow1.reverse()
twoRow2 = deque([1,1,0,0,0,1,1,1, 0]); twoRow2.reverse()
twoRow3 = deque([1,1,0,0,0,1,1,0, 0]); twoRow3.reverse()
twoRow4 = deque([0,0,0,0,1,1,0,0, 0]); twoRow4.reverse()
twoRow5 = deque([0,0,1,1,1,0,0,0, 0]); twoRow5.reverse()
twoRow6 = deque([1,1,1,1,1,1,1,1, 0]); twoRow6.reverse()
twoRow7 = deque([1,1,1,1,1,1,1,1, 0]); twoRow7.reverse()

threeRow0 = deque([1,1,1,1,1,1,1,1, 0]); threeRow0.reverse()
threeRow1 = deque([1,1,1,1,1,1,1,1, 0]); threeRow1.reverse()
threeRow2 = deque([0,0,0,0,1,1,0,0, 0]); threeRow2.reverse()
threeRow3 = deque([0,0,0,1,1,0,0,0, 0]); threeRow3.reverse()
threeRow4 = deque([0,0,0,1,1,0,0,0, 0]); threeRow4.reverse()
threeRow5 = deque([0,0,0,0,1,1,0,0, 0]); threeRow5.reverse()
threeRow6 = deque([1,1,1,1,1,1,1,1, 0]); threeRow6.reverse()
threeRow7 = deque([1,1,1,1,1,1,1,1, 0]); threeRow7.reverse()

fourRow0 = deque([1,1,0,0,0,0,1,1, 0]); fourRow0.reverse()
fourRow1 = deque([1,1,0,0,0,0,1,1, 0]); fourRow1.reverse()
fourRow2 = deque([1,1,0,0,0,0,1,1, 0]); fourRow2.reverse()
fourRow3 = deque([1,1,1,1,1,1,1,1, 0]); fourRow3.reverse()
fourRow4 = deque([1,1,1,1,1,1,1,1, 0]); fourRow4.reverse()
fourRow5 = deque([0,0,0,0,0,0,1,1, 0]); fourRow5.reverse()
fourRow6 = deque([0,0,0,0,0,0,1,1, 0]); fourRow6.reverse()
fourRow7 = deque([0,0,0,0,0,0,1,1, 0]); fourRow7.reverse()

fiveRow0 = deque([1,1,1,1,1,1,1,1, 0]); fiveRow0.reverse()
fiveRow1 = deque([1,1,1,1,1,1,1,1, 0]); fiveRow1.reverse()
fiveRow2 = deque([1,1,0,0,0,0,0,0, 0]); fiveRow2.reverse()
fiveRow3 = deque([1,1,1,1,1,1,1,0, 0]); fiveRow3.reverse()
fiveRow4 = deque([0,0,0,0,0,1,1,0, 0]); fiveRow4.reverse()
fiveRow5 = deque([1,0,0,0,0,0,1,1, 0]); fiveRow5.reverse()
fiveRow6 = deque([1,1,1,1,1,1,1,1, 0]); fiveRow6.reverse()
fiveRow7 = deque([0,0,1,1,1,1,0,0, 0]); fiveRow7.reverse()

sixRow0 = deque([0,1,1,1,1,1,1,0, 0]); sixRow0.reverse()
sixRow1 = deque([1,1,1,1,1,1,1,1, 0]); sixRow1.reverse()
sixRow2 = deque([1,1,0,0,0,0,0,0, 0]); sixRow2.reverse()
sixRow3 = deque([1,1,1,1,1,1,1,1, 0]); sixRow3.reverse()
sixRow4 = deque([1,1,0,0,0,0,1,1, 0]); sixRow4.reverse()
sixRow5 = deque([1,1,0,0,0,0,1,1, 0]); sixRow5.reverse()
sixRow6 = deque([0,1,1,1,1,1,1,0, 0]); sixRow6.reverse()
sixRow7 = deque([0,0,1,1,1,1,0,0, 0]); sixRow7.reverse()

sevenRow0 = deque([1,1,1,1,1,1,1,1, 0]); sevenRow0.reverse()
sevenRow1 = deque([1,1,1,1,1,1,1,1, 0]); sevenRow1.reverse()
sevenRow2 = deque([0,0,0,0,0,1,1,1, 0]); sevenRow2.reverse()
sevenRow3 = deque([0,0,1,1,1,1,1,1, 0]); sevenRow3.reverse()
sevenRow4 = deque([0,0,1,1,1,1,1,0, 0]); sevenRow4.reverse()
sevenRow5 = deque([0,0,1,1,1,0,0,0, 0]); sevenRow5.reverse()
sevenRow6 = deque([0,1,1,1,0,0,0,0, 0]); sevenRow6.reverse()
sevenRow7 = deque([1,1,1,0,0,0,0,0, 0]); sevenRow7.reverse()

eightRow0 = deque([0,0,1,1,1,1,0,0, 0]); eightRow0.reverse()
eightRow1 = deque([1,1,1,0,0,1,1,1, 0]); eightRow1.reverse()
eightRow2 = deque([1,1,1,0,0,1,1,1, 0]); eightRow2.reverse()
eightRow3 = deque([0,1,1,0,0,1,1,0, 0]); eightRow3.reverse()
eightRow4 = deque([0,1,1,1,1,1,1,0, 0]); eightRow4.reverse()
eightRow5 = deque([1,1,1,0,0,1,1,1, 0]); eightRow5.reverse()
eightRow6 = deque([1,1,1,0,0,1,1,1, 0]); eightRow6.reverse()
eightRow7 = deque([0,0,1,1,1,1,0,0, 0]); eightRow7.reverse()

nineRow0 = deque([0,0,1,1,1,1,0,0, 0]); nineRow0.reverse()
nineRow1 = deque([1,1,1,0,0,1,1,1, 0]); nineRow1.reverse()
nineRow2 = deque([1,1,1,0,0,1,1,1, 0]); nineRow2.reverse()
nineRow3 = deque([0,1,1,0,0,1,1,1, 0]); nineRow3.reverse()
nineRow4 = deque([0,1,1,1,1,1,1,1, 0]); nineRow4.reverse()
nineRow5 = deque([0,0,0,0,0,0,1,1, 0]); nineRow5.reverse()
nineRow6 = deque([0,0,0,0,0,0,1,1, 0]); nineRow6.reverse()
nineRow7 = deque([0,0,0,0,0,0,1,1, 0]); nineRow7.reverse()

zeroRow0 = deque([0,0,1,1,1,1,0,0, 0]); zeroRow0.reverse()
zeroRow1 = deque([0,1,1,0,0,1,1,0, 0]); zeroRow1.reverse()
zeroRow2 = deque([1,1,0,0,0,1,1,1, 0]); zeroRow2.reverse()
zeroRow3 = deque([1,1,0,0,1,0,1,1, 0]); zeroRow3.reverse()
zeroRow4 = deque([1,1,0,1,0,0,1,1, 0]); zeroRow4.reverse()
zeroRow5 = deque([1,1,1,0,0,0,1,1, 0]); zeroRow5.reverse()
zeroRow6 = deque([0,1,1,0,0,1,1,0, 0]); zeroRow6.reverse()
zeroRow7 = deque([0,0,1,1,1,1,0,0, 0]); zeroRow7.reverse()

cRow0 = deque([0,0,1,1,1,1,0,0, 0]); cRow0.reverse()
cRow1 = deque([0,1,1,0,0,1,1,0, 0]); cRow1.reverse()
cRow2 = deque([1,1,0,0,0,0,0,0, 0]); cRow2.reverse()
cRow3 = deque([1,1,0,0,0,0,0,0, 0]); cRow3.reverse()
cRow4 = deque([1,1,0,0,0,0,0,0, 0]); cRow4.reverse()
cRow5 = deque([1,1,0,0,0,0,0,0, 0]); cRow5.reverse()
cRow6 = deque([0,1,1,0,0,1,1,0, 0]); cRow6.reverse()
cRow7 = deque([0,0,1,1,1,1,0,0, 0]); cRow7.reverse()

fRow0 = deque([1,1,1,1,1,1,1,1, 0]); fRow0.reverse()
fRow1 = deque([1,1,1,1,1,1,1,1, 0]); fRow1.reverse()
fRow2 = deque([1,1,0,0,0,0,0,0, 0]); fRow2.reverse()
fRow3 = deque([1,1,1,1,1,0,0,0, 0]); fRow3.reverse()
fRow4 = deque([1,1,1,1,1,0,0,0, 0]); fRow4.reverse()
fRow5 = deque([1,1,0,0,0,0,0,0, 0]); fRow5.reverse()
fRow6 = deque([1,1,0,0,0,0,0,0, 0]); fRow6.reverse()
fRow7 = deque([1,1,0,0,0,0,0,0, 0]); fRow7.reverse()

eqRow0 = deque([0,0,0,0,0,0,0,0, 0]); eqRow0.reverse()
eqRow1 = deque([0,3,3,3,3,3,3,0, 0]); eqRow1.reverse()
eqRow2 = deque([0,3,3,3,3,3,3,0, 0]); eqRow2.reverse()
eqRow3 = deque([0,0,0,0,0,0,0,0, 0]); eqRow3.reverse()
eqRow4 = deque([0,0,0,0,0,0,0,0, 0]); eqRow4.reverse()
eqRow5 = deque([0,3,3,3,3,3,3,0, 0]); eqRow5.reverse()
eqRow6 = deque([0,3,3,3,3,3,3,0, 0]); eqRow6.reverse()
eqRow7 = deque([0,0,0,0,0,0,0,0, 0]); eqRow7.reverse()


spaceRow0 = deque([0,0,0,0,0,0,0,0, 0])
spaceRow1 = deque([0,0,0,0,0,0,0,0, 0])
spaceRow2 = deque([0,0,0,0,0,0,0,0, 0])
spaceRow3 = deque([0,0,0,2,2,0,0,0, 0])
spaceRow4 = deque([0,0,0,2,2,0,0,0, 0])
spaceRow5 = deque([0,0,0,0,0,0,0,0, 0])
spaceRow6 = deque([0,0,0,0,0,0,0,0, 0])
spaceRow7 = deque([0,0,0,0,0,0,0,0, 0])


hRow0 = deque([1,1,0,0,0,0,1,1, 0])
hRow1 = deque([1,1,0,0,0,0,1,1, 0])
hRow2 = deque([1,1,0,0,0,0,1,1, 0])
hRow3 = deque([1,1,1,1,1,1,1,1, 0])
hRow4 = deque([1,1,1,1,1,1,1,1, 0])
hRow5 = deque([1,1,0,0,0,0,1,1, 0])
hRow6 = deque([1,1,0,0,0,0,1,1, 0])
hRow7 = deque([1,1,0,0,0,0,1,1, 0])

dotRow0 = deque([0,0,0,0,0,0,0,0, 0])
dotRow1 = deque([0,0,0,0,0,0,0,0, 0])
dotRow2 = deque([0,0,0,0,0,0,0,0, 0])
dotRow3 = deque([0,0,0,0,0,0,0,0, 0])
dotRow4 = deque([0,0,0,0,0,0,0,0, 0])
dotRow5 = deque([0,0,0,0,0,0,0,0, 0])
dotRow6 = deque([0,0,0,1,1,0,0,0, 0])
dotRow7 = deque([0,0,0,1,1,0,0,0, 0])

#Row0 = deque([1, 0])
#Row1 = deque([1, 0])
#Row2 = deque([0, 0])
#Row3 = deque([0, 0])
#Row4 = deque([0, 0])
#Row5 = deque([0, 0])
#Row6 = deque([0, 0])
#Row7 = deque([1, 0])

#for value in smiley:
    # Print each row's length and its elements.
    #    print(len(value), value)

#for x in range(0, 8):

currDeque0 = deque( [0,0,0,0,0,0,0,0, 0])
currDeque1 = deque( [0,0,0,0,0,0,0,0, 0])
currDeque2 = deque( [0,0,0,0,0,0,0,0, 0])
currDeque3 = deque( [0,0,0,0,0,0,0,0, 0])
currDeque4 = deque( [0,0,0,0,0,0,0,0, 0])
currDeque5 = deque( [0,0,0,0,0,0,0,0, 0])
currDeque6 = deque( [0,0,0,0,0,0,0,0, 0])
currDeque7 = deque( [0,0,0,0,0,0,0,0, 0])


#def setSmiley():
#currDeque0 = smileyRow0
#currDeque1 = smileyRow1
#currDeque2 = smileyRow2
#currDeque3 = smileyRow3
#currDeque4 = smileyRow4
#currDeque5 = smileyRow5
#currDeque6 = smileyRow6
#currDeque7 = smileyRow7
#    return;

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


while(True):

	#-----------------------------------------------
	#open the log for reading values
	#-----------------------------------------------
	print "-----=-=-=-------=-  bioreactor-one - montior-one -=---------=-=-=--------"
	tempValFlog = open("/home/pi/curr_F.log", "r");
	print "Opening log...  .", tempValFlog.name, " ...in..", tempValFlog.mode, "..access mode."
	tempValHlog = open("/home/pi/curr_H.log", "r");
	print "Opening log...  .", tempValHlog.name, " ...in..", tempValHlog.mode, "..access mode."
	print "-------=---------=---------------------------------=-----------=----------"
	print " press CTL-Z to exit "
	print "--------------------------------------------------------------------------"
		



	currentF = tempValFlog.read(5)
	currentH = tempValHlog.read(5)

	print currentF
	print currentH
	#===========================================================================
	# design for the led's display is: with a scroll through each option
	#===========================================================================
	#  ______        ___________   _____     _   _          ___  _____  _____
	#  |  ___|_____ |___  / __  \ |____ |   | | | |______  /   ||  ___||  _  |
	#  | |_ |______|   / /`' / /'     / /   | |_| |______|/ /| ||___ \ | |/' |
	#  |  _| ______   / /   / /       \ \   |  _  |______/ /_| |    \ \|  /| |
	#  | |  |______|./ /  ./ /____.___/ /   | | | |______\___  |/\__/ /\ |_/ /
	#  \_|          \_/   \_____(_)____/    \_| |_/          |_/\____(_)\___/
	#
	#===========================================================================

	#first we have to isolate the 100's place, in this case 0
	#if the 100's is 0, then we'll display a space
	#then lets grab the 10's, 1's and the decimal portion.
	#also, we gotta typecast the shit out of this cause of pythons implicit typing...
	hundyPlaceFVal = int(float(currentF) / 100)
	tensPlaceFval = int(float(currentF) / 10)
	onesPlaceFval = int( float(currentF) - (hundyPlaceFVal*100 + tensPlaceFval*10)  )
	decimalPlaceFval = int((float(currentF) - ( hundyPlaceFVal + tensPlaceFval + onesPlaceFval )) * 10)
	decimalPlaceFval /= 100
	#lets see what we got
	print 'F hundy', int(hundyPlaceFVal)
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

	#==========================================================================
	# each message has nineteen characters, | F=123.4 H=100.0 * |
	#==========================================================================
	#lets start with a message index.

	messagelength = 20
	messageindex = 0

	while(messageindex < messagelength):

		if(messageindex == 0):
			currDeque0 = spaceRow0
			currDeque1 = spaceRow1
			currDeque2 = spaceRow2
			currDeque3 = spaceRow3
			currDeque4 = spaceRow4
			currDeque5 = spaceRow5
			currDeque6 = spaceRow6
			currDeque7 = spaceRow7
		elif(messageindex == 1):
			currDeque0 = fRow0
			currDeque1 = fRow1
			currDeque2 = fRow2
			currDeque3 = fRow3
			currDeque4 = fRow4
			currDeque5 = fRow5
			currDeque6 = fRow6
			currDeque7 = fRow7
		elif(messageindex == 2):
			currDeque0 = eqRow0
			currDeque1 = eqRow1
			currDeque2 = eqRow2
			currDeque3 = eqRow3
			currDeque4 = eqRow4
			currDeque5 = eqRow5
			currDeque6 = eqRow6
			currDeque7 = eqRow7

	#begining of Fahrenheight reading

		elif(messageindex == 3):
			if(hundyPlaceFVal == 0):
				currDeque0 = deque( [0,0,0,0,0,0,0,0, 0])
				currDeque1 = deque( [0,0,0,0,0,0,0,0, 0])
				currDeque2 = deque( [0,0,0,0,0,0,0,0, 0])
				currDeque3 = deque( [0,0,0,0,0,0,0,0, 0])
				currDeque4 = deque( [0,0,0,0,0,0,0,0, 0])
				currDeque5 = deque( [0,0,0,0,0,0,0,0, 0])
				currDeque6 = deque( [0,0,0,0,0,0,0,0, 0])
				currDeque7 = deque( [0,0,0,0,0,0,0,0, 0])
			elif(hundyPlaceFVal == 1):
				currDeque0 = oneRow0
				currDeque1 = oneRow1
				currDeque2 = oneRow2
				currDeque3 = oneRow3
				currDeque4 = oneRow4
				currDeque5 = oneRow5
				currDeque6 = oneRow6
				currDeque7 = oneRow7

		elif(messageindex == 4):
			if(tensPlaceFval == 0):
				currDeque0 = zeroRow0
				currDeque1 = zeroRow1
				currDeque2 = zeroRow2
				currDeque3 = zeroRow3
				currDeque4 = zeroRow4
				currDeque5 = zeroRow5
				currDeque6 = zeroRow6
				currDeque7 = zeroRow7
			elif(tensPlaceFval == 1):
				currDeque0 = oneRow0
				currDeque1 = oneRow1
				currDeque2 = oneRow2
				currDeque3 = oneRow3
				currDeque4 = oneRow4
				currDeque5 = oneRow5
				currDeque6 = oneRow6
				currDeque7 = oneRow7
			elif(tensPlaceFval == 2):
				currDeque0 = twoRow0
				currDeque1 = twoRow1
				currDeque2 = twoRow2
				currDeque3 = twoRow3
				currDeque4 = twoRow4
				currDeque5 = twoRow5
				currDeque6 = twoRow6
				currDeque7 = twoRow7
			elif(tensPlaceFval == 3):
				currDeque0 = threeRow0
				currDeque1 = threeRow1
				currDeque2 = threeRow2
				currDeque3 = threeRow3
				currDeque4 = threeRow4
				currDeque5 = threeRow5
				currDeque6 = threeRow6
				currDeque7 = threeRow7
			elif(tensPlaceFval == 4):
				currDeque0 = fourRow0
				currDeque1 = fourRow1
				currDeque2 = fourRow2
				currDeque3 = fourRow3
				currDeque4 = fourRow4
				currDeque5 = fourRow5
				currDeque6 = fourRow6
				currDeque7 = fourRow7
			elif(tensPlaceFval == 5):
				currDeque0 = fiveRow0
				currDeque1 = fiveRow1
				currDeque2 = fiveRow2
				currDeque3 = fiveRow3
				currDeque4 = fiveRow4
				currDeque5 = fiveRow5
				currDeque6 = fiveRow6
				currDeque7 = fiveRow7
			elif(tensPlaceFval == 6):
				currDeque0 = sixRow0
				currDeque1 = sixRow1
				currDeque2 = sixRow2
				currDeque3 = sixRow3
				currDeque4 = sixRow4
				currDeque5 = sixRow5
				currDeque6 = sixRow6
				currDeque7 = sixRow7
			elif(tensPlaceFval == 7):
				currDeque0 = sevenRow0
				currDeque1 = sevenRow1
				currDeque2 = sevenRow2
				currDeque3 = sevenRow3
				currDeque4 = sevenRow4
				currDeque5 = sevenRow5
				currDeque6 = sevenRow6
				currDeque7 = sevenRow7
			elif(tensPlaceFval == 8):
				currDeque0 = eightRow0
				currDeque1 = eightRow1
				currDeque2 = eightRow2
				currDeque3 = eightRow3
				currDeque4 = eightRow4
				currDeque5 = eightRow5
				currDeque6 = eightRow6
				currDeque7 = eightRow7
			elif(tensPlaceFval == 9):
				currDeque0 = nineRow0
				currDeque1 = nineRow1
				currDeque2 = nineRow2
				currDeque3 = nineRow3
				currDeque4 = nineRow4
				currDeque5 = nineRow5
				currDeque6 = nineRow6
				currDeque7 = nineRow7


		elif(messageindex == 5):
			if(onesPlaceFval == 0):
				currDeque0 = zeroRow0
				currDeque1 = zeroRow1
				currDeque2 = zeroRow2
				currDeque3 = zeroRow3
				currDeque4 = zeroRow4
				currDeque5 = zeroRow5
				currDeque6 = zeroRow6
				currDeque7 = zeroRow7
			elif(onesPlaceFval == 1):
				currDeque0 = oneRow0
				currDeque1 = oneRow1
				currDeque2 = oneRow2
				currDeque3 = oneRow3
				currDeque4 = oneRow4
				currDeque5 = oneRow5
				currDeque6 = oneRow6
				currDeque7 = oneRow7
			elif(onesPlaceFval == 2):
				currDeque0 = twoRow0
				currDeque1 = twoRow1
				currDeque2 = twoRow2
				currDeque3 = twoRow3
				currDeque4 = twoRow4
				currDeque5 = twoRow5
				currDeque6 = twoRow6
				currDeque7 = twoRow7
			elif(onesPlaceFval == 3):
				currDeque0 = threeRow0
				currDeque1 = threeRow1
				currDeque2 = threeRow2
				currDeque3 = threeRow3
				currDeque4 = threeRow4
				currDeque5 = threeRow5
				currDeque6 = threeRow6
				currDeque7 = threeRow7
			elif(onesPlaceFval == 4):
				currDeque0 = fourRow0
				currDeque1 = fourRow1
				currDeque2 = fourRow2
				currDeque3 = fourRow3
				currDeque4 = fourRow4
				currDeque5 = fourRow5
				currDeque6 = fourRow6
				currDeque7 = fourRow7
			elif(onesPlaceFval == 5):
				currDeque0 = fiveRow0
				currDeque1 = fiveRow1
				currDeque2 = fiveRow2
				currDeque3 = fiveRow3
				currDeque4 = fiveRow4
				currDeque5 = fiveRow5
				currDeque6 = fiveRow6
				currDeque7 = fiveRow7
			elif(onesPlaceFval == 6):
				currDeque0 = sixRow0
				currDeque1 = sixRow1
				currDeque2 = sixRow2
				currDeque3 = sixRow3
				currDeque4 = sixRow4
				currDeque5 = sixRow5
				currDeque6 = sixRow6
				currDeque7 = sixRow7
			elif(onesPlaceFval == 7):
				currDeque0 = sevenRow0
				currDeque1 = sevenRow1
				currDeque2 = sevenRow2
				currDeque3 = sevenRow3
				currDeque4 = sevenRow4
				currDeque5 = sevenRow5
				currDeque6 = sevenRow6
				currDeque7 = sevenRow7
			elif(onesPlaceFval == 8):
				currDeque0 = eightRow0
				currDeque1 = eightRow1
				currDeque2 = eightRow2
				currDeque3 = eightRow3
				currDeque4 = eightRow4
				currDeque5 = eightRow5
				currDeque6 = eightRow6
				currDeque7 = eightRow7
			elif(onesPlaceFval == 9):
				currDeque0 = nineRow0
				currDeque1 = nineRow1
				currDeque2 = nineRow2
				currDeque3 = nineRow3
				currDeque4 = nineRow4
				currDeque5 = nineRow5
				currDeque6 = nineRow6
				currDeque7 = nineRow7

		elif(messageindex == 6):
				currDeque0 = dotRow0
				currDeque1 = dotRow1
				currDeque2 = dotRow2
				currDeque3 = dotRow3
				currDeque4 = dotRow4
				currDeque5 = dotRow5
				currDeque6 = dotRow6
				currDeque7 = dotRow7

		elif(messageindex == 7):
			if(decimalPlaceFval == 0):
				currDeque0 = zeroRow0
				currDeque1 = zeroRow1
				currDeque2 = zeroRow2
				currDeque3 = zeroRow3
				currDeque4 = zeroRow4
				currDeque5 = zeroRow5
				currDeque6 = zeroRow6
				currDeque7 = zeroRow7
			elif(decimalPlaceFval == 1):
				currDeque0 = oneRow0
				currDeque1 = oneRow1
				currDeque2 = oneRow2
				currDeque3 = oneRow3
				currDeque4 = oneRow4
				currDeque5 = oneRow5
				currDeque6 = oneRow6
				currDeque7 = oneRow7
			elif(decimalPlaceFval == 2):
				currDeque0 = twoRow0
				currDeque1 = twoRow1
				currDeque2 = twoRow2
				currDeque3 = twoRow3
				currDeque4 = twoRow4
				currDeque5 = twoRow5
				currDeque6 = twoRow6
				currDeque7 = twoRow7
			elif(decimalPlaceFval == 3):
				currDeque0 = threeRow0
				currDeque1 = threeRow1
				currDeque2 = threeRow2
				currDeque3 = threeRow3
				currDeque4 = threeRow4
				currDeque5 = threeRow5
				currDeque6 = threeRow6
				currDeque7 = threeRow7
			elif(decimalPlaceFval == 4):
				currDeque0 = fourRow0
				currDeque1 = fourRow1
				currDeque2 = fourRow2
				currDeque3 = fourRow3
				currDeque4 = fourRow4
				currDeque5 = fourRow5
				currDeque6 = fourRow6
				currDeque7 = fourRow7
			elif(decimalPlaceFval == 5):
				currDeque0 = fiveRow0
				currDeque1 = fiveRow1
				currDeque2 = fiveRow2
				currDeque3 = fiveRow3
				currDeque4 = fiveRow4
				currDeque5 = fiveRow5
				currDeque6 = fiveRow6
				currDeque7 = fiveRow7
			elif(decimalPlaceFval == 6):
				currDeque0 = sixRow0
				currDeque1 = sixRow1
				currDeque2 = sixRow2
				currDeque3 = sixRow3
				currDeque4 = sixRow4
				currDeque5 = sixRow5
				currDeque6 = sixRow6
				currDeque7 = sixRow7
			elif(decimalPlaceFval == 7):
				currDeque0 = sevenRow0
				currDeque1 = sevenRow1
				currDeque2 = sevenRow2
				currDeque3 = sevenRow3
				currDeque4 = sevenRow4
				currDeque5 = sevenRow5
				currDeque6 = sevenRow6
				currDeque7 = sevenRow7
			elif(decimalPlaceFval == 8):
				currDeque0 = eightRow0
				currDeque1 = eightRow1
				currDeque2 = eightRow2
				currDeque3 = eightRow3
				currDeque4 = eightRow4
				currDeque5 = eightRow5
				currDeque6 = eightRow6
				currDeque7 = eightRow7
			elif(decimalPlaceFval == 9):
				currDeque0 = nineRow0
				currDeque1 = nineRow1
				currDeque2 = nineRow2
				currDeque3 = nineRow3
				currDeque4 = nineRow4
				currDeque5 = nineRow5
				currDeque6 = nineRow6
				currDeque7 = nineRow7

	# next for the Hydrometer reading

		elif(messageindex == 10):
			currDeque0 = hRow0
			currDeque1 = hRow1
			currDeque2 = hRow2
			currDeque3 = hRow3
			currDeque4 = hRow4
			currDeque5 = hRow5
			currDeque6 = hRow6
			currDeque7 = hRow7
		elif(messageindex == 11):
			currDeque0 = eqRow0
			currDeque1 = eqRow1
			currDeque2 = eqRow2
			currDeque3 = eqRow3
			currDeque4 = eqRow4
			currDeque5 = eqRow5
			currDeque6 = eqRow6
			currDeque7 = eqRow7


		elif(messageindex == 12):
			if(hundyPlaceHval == 0):
				currDeque0 = deque( [0,0,0,0,0,0,0,0, 0])
				currDeque1 = deque( [0,0,0,0,0,0,0,0, 0])
				currDeque2 = deque( [0,0,0,0,0,0,0,0, 0])
				currDeque3 = deque( [0,0,0,0,0,0,0,0, 0])
				currDeque4 = deque( [0,0,0,0,0,0,0,0, 0])
				currDeque5 = deque( [0,0,0,0,0,0,0,0, 0])
				currDeque6 = deque( [0,0,0,0,0,0,0,0, 0])
				currDeque7 = deque( [0,0,0,0,0,0,0,0, 0])
			elif(hundyPlaceHval == 1):
				currDeque0 = oneRow0
				currDeque1 = oneRow1
				currDeque2 = oneRow2
				currDeque3 = oneRow3
				currDeque4 = oneRow4
				currDeque5 = oneRow5
				currDeque6 = oneRow6
				currDeque7 = oneRow7

		elif(messageindex == 13):
			if(tensPlaceHval == 0):
				currDeque0 = zeroRow0
				currDeque1 = zeroRow1
				currDeque2 = zeroRow2
				currDeque3 = zeroRow3
				currDeque4 = zeroRow4
				currDeque5 = zeroRow5
				currDeque6 = zeroRow6
				currDeque7 = zeroRow7
			elif(tensPlaceHval == 1):
				currDeque0 = oneRow0
				currDeque1 = oneRow1
				currDeque2 = oneRow2
				currDeque3 = oneRow3
				currDeque4 = oneRow4
				currDeque5 = oneRow5
				currDeque6 = oneRow6
				currDeque7 = oneRow7
			elif(tensPlaceHval == 2):
				currDeque0 = twoRow0
				currDeque1 = twoRow1
				currDeque2 = twoRow2
				currDeque3 = twoRow3
				currDeque4 = twoRow4
				currDeque5 = twoRow5
				currDeque6 = twoRow6
				currDeque7 = twoRow7
			elif(tensPlaceHval == 3):
				currDeque0 = threeRow0
				currDeque1 = threeRow1
				currDeque2 = threeRow2
				currDeque3 = threeRow3
				currDeque4 = threeRow4
				currDeque5 = threeRow5
				currDeque6 = threeRow6
				currDeque7 = threeRow7
			elif(tensPlaceHval == 4):
				currDeque0 = fourRow0
				currDeque1 = fourRow1
				currDeque2 = fourRow2
				currDeque3 = fourRow3
				currDeque4 = fourRow4
				currDeque5 = fourRow5
				currDeque6 = fourRow6
				currDeque7 = fourRow7
			elif(tensPlaceHval == 5):
				currDeque0 = fiveRow0
				currDeque1 = fiveRow1
				currDeque2 = fiveRow2
				currDeque3 = fiveRow3
				currDeque4 = fiveRow4
				currDeque5 = fiveRow5
				currDeque6 = fiveRow6
				currDeque7 = fiveRow7
			elif(tensPlaceHval == 6):
				currDeque0 = sixRow0
				currDeque1 = sixRow1
				currDeque2 = sixRow2
				currDeque3 = sixRow3
				currDeque4 = sixRow4
				currDeque5 = sixRow5
				currDeque6 = sixRow6
				currDeque7 = sixRow7
			elif(tensPlaceHval == 7):
				currDeque0 = sevenRow0
				currDeque1 = sevenRow1
				currDeque2 = sevenRow2
				currDeque3 = sevenRow3
				currDeque4 = sevenRow4
				currDeque5 = sevenRow5
				currDeque6 = sevenRow6
				currDeque7 = sevenRow7
			elif(tensPlaceHval == 8):
				currDeque0 = eightRow0
				currDeque1 = eightRow1
				currDeque2 = eightRow2
				currDeque3 = eightRow3
				currDeque4 = eightRow4
				currDeque5 = eightRow5
				currDeque6 = eightRow6
				currDeque7 = eightRow7
			elif(tensPlaceHval == 9):
				currDeque0 = nineRow0
				currDeque1 = nineRow1
				currDeque2 = nineRow2
				currDeque3 = nineRow3
				currDeque4 = nineRow4
				currDeque5 = nineRow5
				currDeque6 = nineRow6
				currDeque7 = nineRow7


		elif(messageindex == 14):
			if(onesPlaceHval == 0):
				currDeque0 = zeroRow0
				currDeque1 = zeroRow1
				currDeque2 = zeroRow2
				currDeque3 = zeroRow3
				currDeque4 = zeroRow4
				currDeque5 = zeroRow5
				currDeque6 = zeroRow6
				currDeque7 = zeroRow7
			elif(onesPlaceHval == 1):
				currDeque0 = oneRow0
				currDeque1 = oneRow1
				currDeque2 = oneRow2
				currDeque3 = oneRow3
				currDeque4 = oneRow4
				currDeque5 = oneRow5
				currDeque6 = oneRow6
				currDeque7 = oneRow7
			elif(onesPlaceHval == 2):
				currDeque0 = twoRow0
				currDeque1 = twoRow1
				currDeque2 = twoRow2
				currDeque3 = twoRow3
				currDeque4 = twoRow4
				currDeque5 = twoRow5
				currDeque6 = twoRow6
				currDeque7 = twoRow7
			elif(onesPlaceHval == 3):
				currDeque0 = threeRow0
				currDeque1 = threeRow1
				currDeque2 = threeRow2
				currDeque3 = threeRow3
				currDeque4 = threeRow4
				currDeque5 = threeRow5
				currDeque6 = threeRow6
				currDeque7 = threeRow7
			elif(onesPlaceHval == 4):
				currDeque0 = fourRow0
				currDeque1 = fourRow1
				currDeque2 = fourRow2
				currDeque3 = fourRow3
				currDeque4 = fourRow4
				currDeque5 = fourRow5
				currDeque6 = fourRow6
				currDeque7 = fourRow7
			elif(onesPlaceHval == 5):
				currDeque0 = fiveRow0
				currDeque1 = fiveRow1
				currDeque2 = fiveRow2
				currDeque3 = fiveRow3
				currDeque4 = fiveRow4
				currDeque5 = fiveRow5
				currDeque6 = fiveRow6
				currDeque7 = fiveRow7
			elif(onesPlaceHval == 6):
				currDeque0 = sixRow0
				currDeque1 = sixRow1
				currDeque2 = sixRow2
				currDeque3 = sixRow3
				currDeque4 = sixRow4
				currDeque5 = sixRow5
				currDeque6 = sixRow6
				currDeque7 = sixRow7
			elif(onesPlaceHval == 7):
				currDeque0 = sevenRow0
				currDeque1 = sevenRow1
				currDeque2 = sevenRow2
				currDeque3 = sevenRow3
				currDeque4 = sevenRow4
				currDeque5 = sevenRow5
				currDeque6 = sevenRow6
				currDeque7 = sevenRow7
			elif(onesPlaceHval == 8):
				currDeque0 = eightRow0
				currDeque1 = eightRow1
				currDeque2 = eightRow2
				currDeque3 = eightRow3
				currDeque4 = eightRow4
				currDeque5 = eightRow5
				currDeque6 = eightRow6
				currDeque7 = eightRow7
			elif(onesPlaceHval == 9):
				currDeque0 = nineRow0
				currDeque1 = nineRow1
				currDeque2 = nineRow2
				currDeque3 = nineRow3
				currDeque4 = nineRow4
				currDeque5 = nineRow5
				currDeque6 = nineRow6
				currDeque7 = nineRow7

		elif(messageindex == 15):
				currDeque0 = dotRow0
				currDeque1 = dotRow1
				currDeque2 = dotRow2
				currDeque3 = dotRow3
				currDeque4 = dotRow4
				currDeque5 = dotRow5
				currDeque6 = dotRow6
				currDeque7 = dotRow7

		elif(messageindex == 16):
			if(decimalPlaceHval == 0):
				currDeque0 = zeroRow0
				currDeque1 = zeroRow1
				currDeque2 = zeroRow2
				currDeque3 = zeroRow3
				currDeque4 = zeroRow4
				currDeque5 = zeroRow5
				currDeque6 = zeroRow6
				currDeque7 = zeroRow7
			elif(decimalPlaceHval == 1):
				currDeque0 = oneRow0
				currDeque1 = oneRow1
				currDeque2 = oneRow2
				currDeque3 = oneRow3
				currDeque4 = oneRow4
				currDeque5 = oneRow5
				currDeque6 = oneRow6
				currDeque7 = oneRow7
			elif(decimalPlaceHval == 2):
				currDeque0 = twoRow0
				currDeque1 = twoRow1
				currDeque2 = twoRow2
				currDeque3 = twoRow3
				currDeque4 = twoRow4
				currDeque5 = twoRow5
				currDeque6 = twoRow6
				currDeque7 = twoRow7
			elif(decimalPlaceHval == 3):
				currDeque0 = threeRow0
				currDeque1 = threeRow1
				currDeque2 = threeRow2
				currDeque3 = threeRow3
				currDeque4 = threeRow4
				currDeque5 = threeRow5
				currDeque6 = threeRow6
				currDeque7 = threeRow7
			elif(decimalPlaceHval == 4):
				currDeque0 = fourRow0
				currDeque1 = fourRow1
				currDeque2 = fourRow2
				currDeque3 = fourRow3
				currDeque4 = fourRow4
				currDeque5 = fourRow5
				currDeque6 = fourRow6
				currDeque7 = fourRow7
			elif(decimalPlaceHval == 5):
				currDeque0 = fiveRow0
				currDeque1 = fiveRow1
				currDeque2 = fiveRow2
				currDeque3 = fiveRow3
				currDeque4 = fiveRow4
				currDeque5 = fiveRow5
				currDeque6 = fiveRow6
				currDeque7 = fiveRow7
			elif(decimalPlaceHval == 6):
				currDeque0 = sixRow0
				currDeque1 = sixRow1
				currDeque2 = sixRow2
				currDeque3 = sixRow3
				currDeque4 = sixRow4
				currDeque5 = sixRow5
				currDeque6 = sixRow6
				currDeque7 = sixRow7
			elif(decimalPlaceHval == 7):
				currDeque0 = sevenRow0
				currDeque1 = sevenRow1
				currDeque2 = sevenRow2
				currDeque3 = sevenRow3
				currDeque4 = sevenRow4
				currDeque5 = sevenRow5
				currDeque6 = sevenRow6
				currDeque7 = sevenRow7
			elif(decimalPlaceHval == 8):
				currDeque0 = eightRow0
				currDeque1 = eightRow1
				currDeque2 = eightRow2
				currDeque3 = eightRow3
				currDeque4 = eightRow4
				currDeque5 = eightRow5
				currDeque6 = eightRow6
				currDeque7 = eightRow7
			elif(decimalPlaceHval == 9):
				currDeque0 = nineRow0
				currDeque1 = nineRow1
				currDeque2 = nineRow2
				currDeque3 = nineRow3
				currDeque4 = nineRow4
				currDeque5 = nineRow5
				currDeque6 = nineRow6
				currDeque7 = nineRow7



		else:
			currDeque0 = spaceRow0
			currDeque1 = spaceRow1
			currDeque2 = spaceRow2
			currDeque3 = spaceRow3
			currDeque4 = spaceRow4
			currDeque5 = spaceRow5
			currDeque6 = spaceRow6
			currDeque7 = spaceRow7

		
		
		
		#--031916--deprecated, toggleing each of the deques in the beggining, on their
		# own after running into issue with the characters displaying backwards.. no fun.
		#before outputting, reverse each of the deques since the screen is backwards
		#if(toggle):
		#currDeque0.reverse()
		#currDeque1.reverse()
		#currDeque2.reverse()
		#currDeque3.reverse()
		#currDeque4.reverse()
		#currDeque5.reverse()
		#currDeque6.reverse()
		#currDeque7.reverse()

		while(iter<10):
			iter += 1


			for y in range(0, 8):
				grid.setPixel(0, y, currDeque0[ y ] )
				grid.setPixel(1, y, currDeque1[ y ] )
				grid.setPixel(2, y, currDeque2[ y ] )
				grid.setPixel(3, y, currDeque3[ y ] )
				grid.setPixel(4, y, currDeque4[ y ] )
				grid.setPixel(5, y, currDeque5[ y ] )
				grid.setPixel(6, y, currDeque6[ y ] )
				grid.setPixel(7, y, currDeque7[ y ] )


				#time.sleep(0.02)
			#print ":", iter
			if(toggle):
				currDeque0.rotate(1)
				currDeque1.rotate(1)
				currDeque2.rotate(1)
				currDeque3.rotate(1)
				currDeque4.rotate(1)
				currDeque5.rotate(1)
				currDeque6.rotate(1)
				currDeque7.rotate(1)
						
		messageindex += 1
		iter = 0
		#print 'message index: ', messageindex



	#print grid
	#----------------------------------------------------
	# stored for later use, hopefully it
	# when I eventually build a CloseScript function
	#----------------------------------------------------
	print "Closing log...", tempValFlog.name
	print "Closing log...", tempValHlog.name
	tempValFlog.close()
	tempValHlog.close()
	print " ", tempValFlog.closed
	print " ", tempValHlog.closed

	print 'toggle was: ', toggle
	toggle = not toggle









