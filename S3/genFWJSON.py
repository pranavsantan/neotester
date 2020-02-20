# dependencies

# aws-cli
# curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"
# unzip awscli-bundle.zip
# ./awscli-bundle/install -b ~/bin/aws
# rm -rf aws

# Place latest FW binary in NeoTester/S3 and run script
# Automatically generates .json files for each prefix and syncs local directory with s3
# TestFixture AKIAZC2NNMDHTKFXVI7X LLh5LRkEO8sZcnrSZrQQ8kSG+dAaLC+gG7+vYfku

import os
import platform

str = str(input("Enter Prefixes to update(A,B,C): "))
version = input("Enter the latest Firmware Version: ")

list = str.split(",")

for prefix in list:
	prefix = prefix.strip()
	f = open("firmware{}.json".format(prefix), "w")
	f.write("{\n")
	f.write("\t\"prefix\": \"{}\",\n".format(prefix))
	f.write("\t\"version\": {},\n".format(version))
	f.write("\t\"file\": \"https://neocharge.s3-us-west-1.amazonaws.com/wifi_manager_v{}.bin\"\n".format(version))
	f.write("}")
	f.close()

os.system("~/bin/aws s3 sync . s3://neocharge/ --acl public-read")

# Delete OSx .DS_Store Hidden Files
if platform.system() == 'Darwin':
	os.system("~/bin/aws s3 rm s3://neocharge/.DS_Store")
	os.system("~/bin/aws s3 rm s3://neocharge/._.DS_Store")

quit()

