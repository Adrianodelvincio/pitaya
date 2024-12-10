import sys
import redpitaya_scpi as scpi
import matplotlib.pyplot as plt
import struct
import time
import numpy as np
import os
import subprocess

"This program start the acquisition of signal from channel 1 of the red pitaya 1\
 The acquisition is continuos, namely each signal that trigger is saved. There is a \
 0.5 s of sleep time after a signal is acquired"

IP = '169.254.224.183' # IP address of the pitaya

# Create output directories if they do not exist
os.makedirs("fig_PDS", exist_ok=True)
os.makedirs("data_PDS", exist_ok=True)
os.makedirs("fig_BDS", exist_ok=True)
os.makedirs("data_BDS", exist_ok=True)

try:
    rp_s = scpi.scpi(IP)
except Exception as e:
    print(f"Connection failed: {e}")
    sys.exit(1)

Trigger_level = 0.5 # Volts, default value
ACQTime = 100 # second, acquisiton time
if(len(sys.argv)>2 ):
    Trigger_level = float(sys.argv[2]) # set the trigger value
    ACQTime = int(sys.argv[3])  # total acquisition time

rp_s.tx_txt('ACQ:RST') # Stop the acquisition and reset all acquisition parameters to default values.
rp_s.tx_txt('ACQ:DATA:FORMAT BIN')  # specify data format, only for SCPI
rp_s.tx_txt('ACQ:DATA:Units VOLTS') # specify units
rp_s.tx_txt('ACQ:DEC 1')            # specify decimation, 1 correspond to a buffer of 131.072 us, with 16000 points. The sampling rate is roughly 8 ns
rp_s.tx_txt(f'ACQ:TRig:LEV {Trigger_level}'); print(f'ACQ:TRig:LEV {Trigger_level}')
rp_s.tx_txt('ACQ:START') # start the acquisition

if('CH1' in str(sys.argv[4])):
    rp_s.tx_txt('ACQ:TRig CH1_PE')
elif('CH2' in str(sys.argv[4])):
    rp_s.tx_txt('ACQ:TRig CH2_PE')
else:
    sys.exit(1)

eventlist_PDS = []
eventlist_BDS = []

print("waiting new signal...")
start_time = time.time()
while ((time.time() - start_time) < ACQTime):
    rp_s.tx_txt('ACQ:TRig:STAT?') # check the trigger status
    trigger_status = rp_s.rx_txt()
    if trigger_status == 'TD':
        print("There's a signal!")
        #-----------------------
        ### PDS
        rp_s.tx_txt('ACQ:SOUR1:DATA?')
        buff_byte = rp_s.rx_arb()
        if isinstance(buff_byte, bytes) and len(buff_byte) > 0:
            buff = [struct.unpack('!f',bytearray(buff_byte[i:i+4]))[0] for i in range(0, len(buff_byte), 4)]
            current_time = time.localtime()
            current_date = time.strftime("%Y-%m-%d_%H:%M:%S", current_time)
            filename = f"data_PDS/data-{current_date}.txt"
            eventlist_PDS.append(filename)
            np.savetxt(filename, buff, delimiter = '   ')
            print(f"data saved in {filename}")
            plt.plot(buff[(8192 - 20):(8320)], color = "red" , marker = 'x') # save the data in a plot
            plt.ylabel('Voltage')
            plt.savefig(f"fig_PDS/acquisition-{current_date}.png")
            plt.clf()
        #-----------------------
        ### BDS
        rp_s.tx_txt('ACQ:SOUR2:DATA?')
        buff_byte = rp_s.rx_arb()
        if isinstance(buff_byte, bytes) and len(buff_byte) > 0:
            buff = [struct.unpack('!f',bytearray(buff_byte[i:i+4]))[0] for i in range(0, len(buff_byte), 4)]
            current_time = time.localtime()
            current_date = time.strftime("%Y-%m-%d_%H:%M:%S", current_time)
            filename = f"data_BDS/data-{current_date}.txt"
            eventlist_BDS.append(filename)
            np.savetxt(filename, buff, delimiter = '   ')
            print(f"data saved in {filename}")
            plt.plot(buff[(8192 - 20):(8320)], color = "blue" , marker = 'x') # save the data in a plot
            plt.ylabel('Voltage')
            plt.savefig(f"fig_BDS/acquisition-{current_date}.png")
            plt.clf()
        rp_s.tx_txt('ACQ:RST')                       # reset the acquisition
        rp_s.tx_txt('ACQ:DATA:FORMAT BIN')           # specify data format
        rp_s.tx_txt('ACQ:DATA:Units VOLTS')
        rp_s.tx_txt(f'ACQ:TRig:LEV {Trigger_level}') # load trigger
        rp_s.tx_txt('ACQ:START')                     # start the new acquisition
        if('CH1' in str(sys.argv[4])):
            rp_s.tx_txt('ACQ:TRig CH1_PE')
        elif('CH2' in str(sys.argv[4])):
            rp_s.tx_txt('ACQ:TRig CH2_PE')
        print("waiting new signal...")
        time.sleep(0.1)

# PDS red
for i, item in enumerate(eventlist_PDS):
    subprocess.run(['python3', 'Tutorial/Analysis.py'] + [item] + ['red'])

# BDS blue
for i, item in enumerate(eventlist_BDS):
    subprocess.run(['python3', 'Tutorial/Analysis.py'] + [item] + ['blue'])
