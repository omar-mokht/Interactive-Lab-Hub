
from __future__ import print_function
import qwiic_joystick
import time
import sys

def runExample():

	print("\nSparkFun qwiic Joystick   Example 2\n")
	myJoystick = qwiic_joystick.QwiicJoystick()

	if myJoystick.connected == False:
		print("The Qwiic Joystick device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myJoystick.begin()

	print("Initialized. Firmware Version: %s" % myJoystick.version)

	while True:

		x = myJoystick.horizontal
		y = myJoystick.vertical
		b = myJoystick.button

		if x > 575:
			print("L")
		elif x < 450:
			print("R")

		if y > 575:
			print("U")
		elif y < 450:
			print("D")

		if b == 0:
			print("Button")
			
		time.sleep(0.1)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)