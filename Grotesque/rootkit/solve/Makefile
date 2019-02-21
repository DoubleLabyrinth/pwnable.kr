obj-m += solve.o

all:
	make -C /lib/modules/3.7.1-030701-generic/build M=$(PWD) modules
clean:
	make -C /lib/modules/3.7.1-030701-generic/build M=$(PWD) clean

