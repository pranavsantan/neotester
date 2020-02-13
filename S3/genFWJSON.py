str = str(input("Enter Prefixes to update(A,B,C): "))
version = input("Enter the latest Firmware Version: ")

list = str.split(",")

for prefix in list:
	prefix = prefix.strip()
	f = open("firmware{}.json".format(prefix), "w")
	f.write("{\n")
	f.write("\t\"version\": {},\n".format(version))
	f.write("\t\"file\": \"https://neocharge.s3-us-west-1.amazonaws.com/wifi_manager_v{}.bin\n".format(version))
	f.write("}")
	f.close()

quit()

