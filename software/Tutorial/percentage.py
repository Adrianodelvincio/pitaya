#!/usr/bin/env python3

import sys
import redpitaya_scpi as scpi

IP = '169.254.224.183'
rp_s = scpi.scpi(IP)

if (len(sys.argv) > 2):
    percent = int(sys.argv[2])
else:
    percent = 50

print ("Bar showing "+str(percent)+"%")

for i in range(8):
    if (percent > (i * (100.0/8))):
        rp_s.tx_txt('DIG:PIN LED' + str(i) + ',' + str(1))
    else:
        rp_s.tx_txt('DIG:PIN LED' + str(i) + ',' + str(0))

rp_s.close()
