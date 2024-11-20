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