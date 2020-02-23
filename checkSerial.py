# Reset FTDI Device and open Serial with autoreset
# Find and print Serial Number and FW Version

import os
import platform
import fcntl
import serial
import re

from config import pwd, FTDIport, currFW

# run resetFTDI Script as SUDO and enable RW access to Serial Ports
def resetFTDI():
    os.system("echo {pwd} | sudo -S python3 resetFTDI.py")
    os.system("echo {pwd} | sudo -S chmod a+rw /dev/ttyUSB0 /dev/ttyUSB1")

# Open Serial port
def initSerial():
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.port = FTDIport
    ser.timeout = 1
    ser.rts = False
    ser.dtr = False
    ser.open()
    return ser

# Read Serial lines to find FW Version and Serial Number
def checkFW():
    fw = 0
    sn = ""
    ser = initSerial()
    cont = True
    while(cont):
        line = str(ser.readline())
        line = line[line.find("0;32mI ")+len("0;32mI ") : line.rfind("\\x1b")]

        if 'STATE: Idle' in line:
            cont = False
        if 'Serial No:' in line:
            sn = line[line.find("Serial No:: ")+len("Serial No:: "):]
            print("Serial No: {}".format(sn))
        if 'Firmware' in line:
            fw = int(line[line.find("Firmware ")+len("Firmware "):])
            print("Firmware Version: {}".format(fw))
    ser.close()
    return fw, sn

resetFTDI()
fw, sn = checkFW()

if(fw < currFW):
    print("Current FW(v{}) older than Latest FW(v{})".format(fw, currFW))
    os.system("python ~/esp/esp-idf/components/esptool_py/esptool/esptool.py --chip esp32 -p {} -b 921600 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 40m --flash_size detect 0xd000 ~/esp/NeoTester/flash/ota_data_initial.bin 0x1000 ~/esp/NeoTester/flash/bootloader.bin 0x10000 ~/esp/NeoTester/S3/wifi_manager_v{}.bin  0x8000 ~/esp/NeoTester/flash/partitions.bin".format(FTDIport, currFW))
    checkFW()
else:
    print("Firmware up to date (v{} >= v{})".format(fw, currFW))