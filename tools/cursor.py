#! python3

import pyautogui
import time

#pyautogui.PAUSE = 1
#pyautogui.FAILSAFE = True

with open('cursor.txt', 'w') as file:
	i = 0
	while True:
		time.sleep(0.01)
		i += 1
		# Get and print the mouse coordinates.
		try:
			x, y = pyautogui.position()
			file.write("%s, %s \n" % (x,y))
			positionStr = 'X: ' + str(x).rjust(5) + ' Y: ' + str(y).rjust(5)
			print(positionStr, end='')
			print('\b' * len(positionStr), end='', flush=True)
		except KeyboardInterrupt:
			print('\nDone.')
			print(i)
