#! python3

import pyautogui

#pyautogui.PAUSE = 1
#pyautogui.FAILSAFE = True


while True:
	# Get and print the mouse coordinates.
	try:
		x, y = pyautogui.position()
		positionStr = 'X: ' + str(x).rjust(5) + ' Y: ' + str(y).rjust(5)
		print(positionStr, end='')
		print('\b' * len(positionStr), end='', flush=True)
	except KeyboardInterrupt:
		print('\nDone.')
