#!/bin/sh

read file
echo "Burn file '$file'"

esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 921600 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 40m --flash_size detect 0xd000 ~/esp/wifi_manager/build/ota_data_initial.bin 0x1000 ~/esp/wifi_manager/build/bootloader/bootloader.bin 0x10000 ~/esp/wifi_manager/S3/wifi_manager_v1402.bin 0x8000 ~/esp/wifi_manager/build/partitions.bin

echo "Ready to Run:"
echo "echo "BURN" | espefuse.py -b 115200 -p /dev/ttyUSB0 burn_block_data BLK3 $file"
echo "espefuse.py -b 115200 -p /dev/ttyUSB0 dump"
echo "rm $file"

