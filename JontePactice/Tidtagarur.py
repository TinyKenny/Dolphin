import datetime
import time

sekunder = 0
minuter = 0
timmar = 0
dagar = 0



print ("wait two")
time.sleep (1)
print ("two waited")
time.sleep (1)
print (datetime.datetime.now())
print ("and now begins the shittage")

while True:
	time.sleep (1)
	sekunder += 1
	if (sekunder == 60):
		sekunder = 0
		minuter += 1
		if (minuter == 60):
			minuter = 0
			timmar += 1
			if (timmar == 24):
				timmar = 0
				dagar += 1
	print (dagar, "dagar", timmar, "timmar", minuter, "minuter och", sekunder, "sekunder")


