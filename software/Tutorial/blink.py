import sys
import time
import numpy as np
import redpitaya_scpi as scpi

IP = '169.254.224.183' # local IP of the machine
rp_s = scpi.scpi(IP)

if (len(sys.argv) > 2):
    led = int(sys.argv[2])
else:
    led = 0

print ("Blinking LED["+str(led)+"]")

period = 1 # seconds

start_time = time.time()
count = 0

while (time.time()- start_time < 30):
        random = str(int(np.random.uniform(0,8)))
        print(f"BLINKING LED {random}")
        time.sleep(period/2.0)
        rp_s.tx_txt('DIG:PIN LED' + random +',' + str(1))
        time.sleep(period/2.0)
        rp_s.tx_txt('DIG:PIN LED' + random +',' + str(0))

rp_s.close()