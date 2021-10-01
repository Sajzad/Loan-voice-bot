import pandas as pd
from voice_bot import outgoing_call
import voice_bot





with open("ount.txt", "r") as f:
    count = int(f.read().strip())

try:
	while  True:
		outgoing_call(count)
		count+=1
except Exception as e:
	print(e)
except KeyboardInterrupt as e:
	print(e)

with open("count.txt", "w") as f:
	f.write(str(count))