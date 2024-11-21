#--------------------------
Author: Adriano Del Vincio
#--------------------------

This folder contains the data acquisition software of the scintillators to measure the plasma lenght (BURRITOS SYSTEM)
To communicate with the RedPitaya, we are using the SCPI protocol (Standard Commands for Programmable Instrumentation)


To Start the SCPI in red pitaya, use the following commands:



ssh root@___ip___
password root
systemctl stop redpitaya_nginx
systemctl start redpitaya_scpi &

this will start the SCPI connection.

#- - - - - -
red pitaya 1: '169.254.224.183'
red pitaya 2: 
#- - - - - -

Once the acquisition has started, you start the acqusition with two scripts:

python3 ExtTrigger.py - 0.150 3600

the first argument, 0.150, is the trigger value given in Volts, the second argument, 3600, is the total time of the acquisition, given in seconds.
This script will start the acquisition with an external trigger. Every time the trigger condition is met, the script save the data in 'data/' folder and will create a plot
with the signal.