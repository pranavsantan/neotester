import os
import fcntl
import subprocess


def resetFTDI():
    # Equivalent of the _IO('U', 20) constant in the linux kernel.
    USBDEVFS_RESET = ord('U') << (4*2) | 20

    # Get Devfs of FTDI Devices
    listdev = str(subprocess.check_output("lsusb | grep 0403:6015", shell=True)).split("\\n")

    for device in listdev:
        if(len(device) < 10):
            break

        bus = device[device.find("Bus ")+len("Bus "): device.find(" Device")]
        dev = device[device.find("Device ")+len("Device "): device.find(": ID")]

        # open USB Device
        fd = os.open("/dev/bus/usb/{}/{}".format(bus, dev), os.O_WRONLY)

        # reset USB Device
        try:
            fcntl.ioctl(fd, USBDEVFS_RESET, 0)
        finally:
            os.close(fd)
        print("Successfully Reset dev:{} bus:{}".format(dev, bus))

resetFTDI()