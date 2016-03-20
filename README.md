# raspberrypi-bioreactorproject
Raspberry Pi BioReactor code for temperature and humidity monitoring, with display on the Adafruit 8x8 LED Matrix

Hey yall in the internet land, uploading this mostly for future reference, and because making an entire font library in one-dimensional lists
in python has been an excruciating excercise in patience, but, here it is!

PLEASE CHECK THE SOURCE CODE FOR COMMENTS ON HOW IT ALL WORKS

First, get the LED Backpack library from Adafruits website: 

https://learn.adafruit.com/adafruit-led-backpack/overview

Then, follow the instructions for setting up a python dev environment, I used the ones for the 
webIDE since it adds the ability to browse your raspberry pi from the network. Personally, I use XCode to edit the 
source code, but whichever environment suits you the best. 

https://learn.adafruit.com/webide/overview

Then, the sensor I'm using is the DHT11, I know, I know, the DHT22 is soo much better. Yup, it was also 2 dollars better, 
and 2 dollars buys a lot of hot dogs when your a grad student. In my hot dogs defense, the sensor has only been off by 
a few degrees,  which is fine for me. I'm not cooking meth in a fractional distillation here, I'm making an overgrown 
thermometer that looks cool and I can use to complain to my land owner about how crappy the AC is in the house. 

https://www.adafruit.com/product/386

Ok so how this works: 

<> Grab the reading from the themometer. 
<> Update the reading once a minute through the crontab into a log file. 
<> Split that reading into two log files, one for fahrenheight, and one for humidity. 
<> Chop that value into characters to output to the LED screen
<> Add our script to run on reboot. 
<> Complain to landlord that the AC is too hot. This is Vegas, dude. 
