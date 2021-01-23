obj-m += step_moter.o
#ccflags-y += -mfloat-abi=hard
LDLIBS += -lgcc_s

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules
clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean

table:
	python3 step_moter.py > step_tab.h

unload:
	rmmod step_moter.ko
load:
	insmod step_moter.ko
	sleep 0.5
	chmod 666 /dev/step_moter0