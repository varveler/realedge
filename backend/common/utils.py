
import random
import time

def wait_random_seconds(min=2, max=4):
	rand_time = random.randint(min, max)
	print('Waiting %s Seconds...' % rand_time)
	time.sleep(rand_time)

def atr(df, n=14):
    data = df.copy()
    high = data['high']
    low = data['low']
    close = data['close']
    data['tr0'] = abs(high - low)
    data['tr1'] = abs(high - close.shift())
    data['tr2'] = abs(low - close.shift())
    tr = data[['tr0', 'tr1', 'tr2']].max(axis=1)
    atr = wwma(tr, n)
    return atr