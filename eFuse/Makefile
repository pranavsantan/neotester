CC = gcc
CFLAGS = -g -Wall
LIBS = -lstdc++

#append a 32 to executable name if on a 32 bit machine
FILE = 
ARCH = $(shell arch)
ifeq ("$(ARCH)", "i686")
	FILE = 32
endif

SRC = eFuse.c 

all:  eFuse$(FILE)

efuse$(FILE): eFuse.c $(SRC)
	$(CC) $(CFLAGS) -o eFuse$(FILE) $(SRC) $(LIBS)

cleano:
	rm -f *.o

clean:
	rm -f eFuse *.o

