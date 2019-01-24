import sys
import time
from threading import Thread
import Movuino as mvn

#####################################################################
####################		MOVUINOS			#####################
#####################################################################

# COMPUTER
computerIP = "172.20.10.3" # set here your computer IP

# MOVUINO MASTER
movuinoIPMst = "172.20.10.4"  # set here your Movuino master IP once its connected to the same wifi network as your computer
movuinoMst = mvn.Movuino(computerIP, movuinoIPMst, 7400, 7401) # 7400 port out // 7401 port in

# MOVUINO SLAVE
movuinoIPSlv = "172.20.10.5"  # set here your Movuino slave IP once its connected to the same wifi network as your computer
movuinoSlv = mvn.Movuino(computerIP, movuinoIPSlv, 7500, 7501)

#-----------------------#

def setMovuinosNeopix(mvn1_, mvn2_, red_, green_, blue_):
	mvn1_.setNeoPix(red_, green_, blue_)
	mvn2_.setNeoPix(red_, green_, blue_)

def printMovuinoData(mvn_):
	print "Movuino ID:", mvn_.id
	print "Accelerometer data:", mvn_.ax, mvn_.ay, mvn_.az
	print "Gyroscope data:", mvn_.gx, mvn_.gy, mvn_.gz
	print "Magnetometer data:", mvn_.mx, mvn_.my, mvn_.mz
	print "---"

#####################################################################
####################		 MAIN				#####################
#####################################################################
def main(args = None):
	movuinoMst.start() # start thread and OSC communication
	movuinoSlv.start()

	#-----------------------#

	movuinoMst.vibroNow(True)       # activate vibration on Movuino master
	movuinoMst.setNeoPix(255,0,0)   # set pixel color on Movuino master
	movuinoSlv.setNeoPix(0,0,255)   # set pixel color on Movuino slave
	time.sleep(0.5)
	movuinoMst.vibroNow(False)      # turn off vibration on Movuino master

	timer0 = time.time()
	while (time.time()-timer0 < 5):
		printMovuinoData(movuinoSlv)

		red_ = (int)(255.0*(0.07+movuinoMst.ax)/0.14)     # set red light component
		green_ = (int)(255.0*(0.07+movuinoMst.ay)/0.14)   # set green
		blue_ = 0                                         # set blue

		setMovuinosNeopix(movuinoMst, movuinoSlv, red_, green_, blue_)  # set pixel color on both Movuino

		time.sleep(.01) # let quick sleep to avoid overload
	
	movuinoMst.vibroPulse(150,100,3)                        # make pulsation on Movuino master (vibration time, vibration off, number of pulsation)
	setMovuinosNeopix(movuinoMst, movuinoSlv, 0,255,0)

	movuinoMst.lightNow(False) # turn off light on Movuino Master
	time.sleep(0.5)
	movuinoMst.lightNow(True)  # turn on on last color
	time.sleep(0.5)
	movuinoMst.lightNow(False)

	#-----------------------#

	movuinoMst.stop() # stop thread and OSC communication
	movuinoSlv.stop()

if __name__ == '__main__':
	sys.exit(main())