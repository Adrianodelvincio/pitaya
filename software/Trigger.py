import sys
import redpitaya_scpi as scpi
import matplotlib.pyplot as plt
import struct
import time
import numpy as np
import subprocess

"This program start the acquisition of signal from channel 1 of the red pitaya 1\
 The acquisition is continuos, namely each signal that trigger is saved. There is a \
 0.5 s of sleep time after a signal is acquired"


IP = '169.254.224.183' # IP address of the pitaya

Trigger_level = 0.5 # Volts, default value
ACQTime = 100 # second, acquisiton time
if(len(sys.argv)>2 ):
    Trigger_level = sys.argv[2] # set the trigger value
    ACQTime = int(sys.argv[3])  # total acquisition time

rp_s = scpi.scpi(IP) # Initialize connection with IP

rp_s.tx_txt('ACQ:RST') # Stop the acquisition and reset all acquisition parameters to default values.
rp_s.tx_txt('ACQ:DATA:FORMAT BIN')  # specify data format, only for SCPI
rp_s.tx_txt('ACQ:DATA:Units VOLTS') # specify units
rp_s.tx_txt('ACQ:DEC 1')            # specify decimation, 1 correspond to a buffer of 131.072 us, with 16000 points. The sampling rate is roughly 8 ns
rp_s.tx_txt(f'ACQ:TRig:LEV {Trigger_level}'); print(f'ACQ:TRig:LEV {Trigger_level}')
rp_s.tx_txt('ACQ:START') # start the acquisition
rp_s.tx_txt('ACQ:TRig CH1_PE')


eventlist = []
print("waiting new signal...")
start_time = time.time()
while ((time.time() - start_time) < ACQTime):
    rp_s.tx_txt('ACQ:TRig:STAT?') # check the trigger status
    if rp_s.rx_txt() == 'TD':
        print("There's a signal!")
        rp_s.tx_txt('ACQ:SOUR1:DATA?')
        buff_byte = rp_s.rx_arb()
        if isinstance(buff_byte, bytes) and len(buff_byte) > 0:
            buff = [struct.unpack('!f',bytearray(buff_byte[i:i+4]))[0] for i in range(0, len(buff_byte), 4)]
            current_time = time.localtime()
            current_date = time.strftime("%Y-%m-%d_%H:%M:%S", current_time)
            filename = f"data/data-{current_date}.txt"
            eventlist.append(filename)
            np.savetxt(filename, buff, delimiter = '   ')
            print(f"data saved in {filename}")
            plt.plot(buff[(8192 - 20):(8320)], color = "red" , marker = 'x') # save the data in a plot
            plt.ylabel('Voltage')
            plt.savefig(f"fig/acquisition-{current_date}.png")
            plt.clf()
        rp_s.tx_txt('ACQ:RST')                       # reset the acquisition
        rp_s.tx_txt('ACQ:DATA:FORMAT BIN')           # specify data format
        rp_s.tx_txt('ACQ:DATA:Units VOLTS')
        rp_s.tx_txt(f'ACQ:TRig:LEV {Trigger_level}') # load trigger
        rp_s.tx_txt('ACQ:START')                     # start the new acquisition
        print("waiting new signal...")
        rp_s.tx_txt('ACQ:TRig CH1_PE')
        time.sleep(0.5)

for i, item in enumerate(eventlist):
    subprocess.run(['python3', 'Tutorial/Analysis.py'] + [item])