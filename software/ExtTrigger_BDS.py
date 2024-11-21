import sys
import redpitaya_scpi as scpi
import matplotlib.pyplot as plt
import numpy as np
import time
import os
import subprocess

"This program start the acquisition of signal from channel 1 of the red pitaya 1\
 The acquisition is triggered by an External trigger There is a \
 0.5 s of sleep time after a signal is acquired"

IP = '169.254.224.183'

rp_s = 0

# Create output directories if they do not exist
os.makedirs("fig_BDS", exist_ok=True)
os.makedirs("data_BDS", exist_ok=True)

try:
    rp_s = scpi.scpi(IP)
except Exception as e:
    print(f"Connection failed: {e}")
    sys.exit(1)

rp_s.tx_txt('ACQ:RST')
rp_s.tx_txt('ACQ:DEC 1')

# For short triggering signals set the length of internal debounce filter in us (minimum of 1 us)
rp_s.tx_txt('ACQ:TRig:EXT:DEBouncerUs 10')
rp_s.tx_txt('ACQ:START')
rp_s.tx_txt('ACQ:TRig EXT_PE')

Trigger_level = 0.5 # Volts, default value
ACQTime = 100 # second, acquisiton time
if(len(sys.argv)> 2 ):
    Trigger_level = sys.argv[2] # set the trigger value
    ACQTime = int(sys.argv[3])  # total acquisition time
    print(f"Trigger set to {Trigger_level}")
else:
    print(f"default trigger level {Trigger_level}")
    print(f"default ACQ time {ACQTime}")

rp_s.tx_txt(f"ACQ:TRIG:LEV {Trigger_level}")

eventlist = []

start_time = time.time()
print("waiting for external trigger")
while ((time.time() - start_time) < ACQTime):
    rp_s.tx_txt('ACQ:TRig:STAT?')
    if rp_s.rx_txt() == 'TD':
        print("There's a signal")
        rp_s.tx_txt('ACQ:SOUR2:DATA?')
        buff_string = rp_s.rx_txt() # get the data
        buff_string = buff_string.strip('{}\n\r').replace("  ", "").split(',')
        buff = list(map(float, buff_string))
        plt.plot(buff[(8192 - 20):(8320)], color = "blue" , marker = 'x'); plt.ylabel('Voltage')# save the data in a plot
        current_time = time.localtime()
        current_date = time.strftime("%Y-%m-%d_%H-%M-%S", current_time)
        plt.savefig(f"fig_BDS/acquisition-{current_date}.png"); plt.clf()
        filename = f"data_BDS/data-{current_date}.txt"
        eventlist.append(filename) # append to list of signals
        np.savetxt(filename, buff, delimiter = '   ') ; print(f"data saved in {filename}")
        ### new acquisition
        rp_s.tx_txt('ACQ:RST')                       # reset the acquisition
        rp_s.tx_txt('ACQ:START')                     # start the acquisition
        rp_s.tx_txt('ACQ:TRig EXT_PE')               # define the external trigger
        rp_s.tx_txt(f"ACQ:TRIG:LEV {Trigger_level}") # set the trigger value
        print("waiting for external trigger")

for i, item in enumerate(eventlist):
    subprocess.run(['python3', 'Tutorial/Analysis.py'] + [item] + ['blue'])
