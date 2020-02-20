#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

// Configuration struct
typedef struct __attribute__((__packed__)) Config_t{
	uint8_t curr; // Current Limit
	uint32_t date; // Production Date
	char pre[4]; // Type Prefix (UL, BETA2, ETC)
	uint32_t serial; // 32 Bit Unique Device Identifier
	char pad[19];
}Config_t;

Config_t *checkArgs(int argc, char *argv[]);

Config_t *initConfig(){
	Config_t *c = malloc(sizeof(Config_t));

	if(c == NULL)
		printf("Malloc Failed");
        
	c->curr = 30;
	c->date = 190924;
	strncpy(c->pre, "PS", 4);
   	c->serial = 2;
	strncpy(c->pad, "\0", 19);
	return c;
}

char* toSerialString(Config_t *config){
	char *ret = malloc(32);
	sprintf(ret, "NC:%02u:%06u:%s:%08u", config->curr, config->date, config->pre, config->serial);
	return ret;
}

int main(int argc, char *argv[]) {
	Config_t *config = checkArgs(argc, argv);//initConfig();
	FILE *write_ptr;
	char fileName[16];
//	struct Config_t structVar = {30,190820,"B2", 0xDEADBEEF};
//	struct Config_t* strucPtr = &structVar;
	
	// Print Payload Bitwise in Hex
	unsigned char* charPtr = (unsigned char*)config;
	for(int i = 0; i < sizeof(Config_t); i++){
		printf("%02X",charPtr[i]);
	}
	
	sprintf(fileName, "%s%08u.bin", config->pre, config->serial);
	write_ptr = fopen(fileName,"wb");  // w for write, b for binary
	printf("\n");

	fwrite(config, 32, 1, write_ptr); // write 32 bytes from config struct
	
	char cmd[1024] = "";
	sprintf(cmd, "echo \"%s\" | sh burn.sh", fileName);
	system(cmd);
}

Config_t *checkArgs(int argc, char *argv[]){
	Config_t *c = malloc(sizeof(Config_t));
	if(c == NULL)
		printf("Malloc Failed");

	if (argc != 5){
		fprintf(stderr, "Usage %s Date:[YYMMDD] Current:[30/50] Prefix:[XXXX] Serial:[00000000]\n", argv[0]);
		exit(-1);
	}
	
	c->date = atoi(argv[1]);
	c->curr = atoi(argv[2]);
	strncpy(c->pre, argv[3], 4);
	c->serial = atoi(argv[4]);
	strncpy(c->pad, "\0", 19);
	
	printf("%s\n", toSerialString(c));
	
	return c;
}

//cd ~/esp/esp-idf
//./install.sh
//. ./export.sh
//espefuse.py -b 115200 -p /dev/cu.usbserial-DN05T01F  burn_block_data BLK3 ~/esp/wifi_manager/eFuse/1B200000005.bin 