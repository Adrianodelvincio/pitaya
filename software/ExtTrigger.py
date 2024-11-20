import sys
import redpitaya_scpi as scpi
import matplotlib.pyplot as plt
import numpy as np
import time

IP = '169.254.224.183'

rp_s = scpi.scpi(IP)

rp_s.tx_txt('ACQ:RST')

rp_s.tx_txt('ACQ:DEC 1')

# For short triggering signals set the length of internal debounce filter in us (minimum of 1 us)
rp_s.tx_txt('ACQ:TRig:EXT:DEBouncerUs 10')

rp_s.tx_txt('ACQ:START')
rp_s.tx_txt('ACQ:TRig EXT_PE')

Trigger_level = 0.5 # Volts, default value

if(len(sys.argv)> 2 ):
    Trigger_level = sys.argv[2] # set the trigger value
    print(f"Trigger set to {Trigger_level}")
else:
    print(f"default trigger level {Trigger_level}")

rp_s.tx_txt(f"ACQ:TRIG:LEV {Trigger_level}")


start_time = time.time()
print("waiting for external trigger")
while ((time.time() - start_time) < int(sys.argv[3])):
    rp_s.tx_txt('ACQ:TRig:STAT?')
    if rp_s.rx_txt() == 'TD':
        print("There's a signal")
        rp_s.tx_txt('ACQ:SOUR1:DATA?')
        buff_string = rp_s.rx_txt() # get the data
        buff_string = buff_string.strip('{}\n\r').replace("  ", "").split(',')
        buff = list(map(float, buff_string))
        plt.plot(buff[(8192 - 20):(8320)], color = "blue" , marker = 'x'); plt.ylabel('Voltage')# save the data in a plot
        current_time = time.localtime()
        current_date = time.strftime("%Y-%m-%d_%H-%M-%S", current_time)
        plt.savefig(f"fig/acquisition-{current_date}.png"); plt.clf()
        filename = f"data/data-{current_date}.txt"
        np.savetxt(filename, buff, delimiter = '   ')
        print(f"data saved in {filename}")
        ### new acquisition
        rp_s.tx_txt('ACQ:RST')                       # reset the acquisition
        rp_s.tx_txt('ACQ:START')
        rp_s.tx_txt('ACQ:TRig EXT_PE')
        rp_s.tx_txt(f"ACQ:TRIG:LEV {Trigger_level}")
        print("waiting for external trigger")