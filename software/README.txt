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
red pitaya 2: '169.254.42.255'
red pitaya 3: ''
#- - - - - -

Once the acquisition has started, you start the acqusition with two scripts:

python3 ExtTrigger.py - 0.150 3600

the first argument, 0.150, is the trigger value given in Volts, the second argument, 3600, is the total time of the acquisition, given in seconds.
This script will start the acquisition with an external trigger. Every time the trigger condition is met, the script save the data in 'data/' folder and will create a plot
with the signal.

- - - - - - -

1 scintillator, Rf 1.1kohm at the PDS
1 scintillator, Rf 3.3kHz at the BDS
1 scintillator, Rf 1.1kHz at the UP-ATDS

PDS and BDS go to red pitaya 1 (169.254.224.183)

red pitaya 1 not in the zone
red pitaya 2 not in the zone


Inventario.
Fare setup con macchina che ci da INA.
Installare due scintillatori alla PDS, da 1k, uno fisso e uno mobile.
Sincronizzazione.