# %%

import pyautogui
import time
import datetime

orders_path = 'C:\\Users\dellg3\Documents\Trading\Records\Orders'
trades_path = 'C:\\Users\dellg3\Documents\Trading\Records\Trades'

pyautogui.click(970, 990,)
pyautogui.click(button='right', x=970, y=900)
pyautogui.click(1030, 930,)
time.sleep(2)
pyautogui.hotkey('tab', interval=0.2)
pyautogui.hotkey('tab', interval=0.2)
pyautogui.hotkey('tab', interval=0.2)       
pyautogui.hotkey('tab', interval=0.2)
pyautogui.hotkey('tab', interval=0.2)
pyautogui.hotkey('tab', interval=0.2)
pyautogui.hotkey('enter', interval=0.1)
pyautogui.hotkey('backspace', interval=0.1)
pyautogui.write(orders_path)
pyautogui.hotkey('enter', interval=0.2)
pyautogui.hotkey('alt', 'n',)
date = datetime.datetime.now().strftime("%m-%d-%y")
pyautogui.write(date + '-Orders')
pyautogui.hotkey('tab', interval=0.1)
pyautogui.hotkey('tab', interval=0.1)
pyautogui.hotkey('tab', interval=0.1)
pyautogui.hotkey('enter', interval=0.1)
pyautogui.click(770, 990,)
pyautogui.click(button='right', x=970, y=900)
time.sleep(0.5)
pyautogui.click(1030, 980,)
time.sleep(2)
pyautogui.hotkey('tab', interval=0.2)
pyautogui.hotkey('tab', interval=0.2)
pyautogui.hotkey('tab', interval=0.2)       
pyautogui.hotkey('tab', interval=0.2)
pyautogui.hotkey('tab', interval=0.2)
pyautogui.hotkey('tab', interval=0.2)
pyautogui.hotkey('enter', interval=0.1)
pyautogui.hotkey('backspace', interval=0.1)
pyautogui.write(trades_path)
pyautogui.hotkey('enter', interval=0.2)
pyautogui.hotkey('alt', 'n',)
date = datetime.datetime.now().strftime("%m-%d-%y")
pyautogui.write(date + '-Trades')
pyautogui.hotkey('tab', interval=0.1)
pyautogui.hotkey('tab', interval=0.1)
pyautogui.hotkey('tab', interval=0.1)
pyautogui.hotkey('enter', interval=0.1)

