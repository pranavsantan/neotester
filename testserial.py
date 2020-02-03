# Reading PZEM-004t power sensor (new version v3.0) through Modbus-RTU protocol over TTL UART
# Run as:
# python3 pzem_004t.py

# To install dependencies: 
# pip install modbus-tk
# pip install pyserial

import time
import os
from subprocess import call

import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

def clear():
	_ = call('clear' if os.name == 'posix' else 'cls')

def initModbus(serial):
	# Connect to the slave
	master = modbus_rtu.RtuMaster(serial)
	master.set_timeout(2.0)
	master.set_verbose(True)

	data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)
	
	return master

def readVIR(master):
	data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)

	voltage = data[0] / 10.000 # [V]
	voltage = round((voltage + 0.293) / 403.17, 3) # Modified voltage to read Step Down Output (0.000 - 0.800VAC)
	current = (data[1] + (data[2] << 16)) / 1000.0 # [A]
	resistance = "inf"
	if current > 0:
		resistance = round((voltage * 1000) / current , 3) # Calculate Resistance in mOhm
	power = (data[3] + (data[4] << 16)) / 10.0 # [W]
	energy = data[5] + (data[6] << 16) # [Wh]
	frequency = data[7] / 10.0 # [Hz]
	powerFactor = data[8] / 100.0
	alarm = data[9] # 0 = no alarm
	
	return voltage, current, resistance;


serial = serial.Serial(port='/dev/ttyUSB1', baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0)
master = initModbus(serial);
while True:
	voltage, current, resistance = readVIR(master)
	clear()	
	print('Voltage [V]: ', voltage)
	print('Current [A]: ', current)
	print('Resistance [mOhm]: ', resistance)
	time.sleep(0.5)

try:
    master.close()
    if slave.is_open:
        slave.close()
except:
    pass

