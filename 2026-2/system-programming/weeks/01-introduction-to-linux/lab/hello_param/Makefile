obj-m += hello_param.o

# Override KDIR when building against headers for a kernel that is not the
# one currently running (e.g., inside a container):
#   make KDIR=/usr/src/linux-headers-<version>-generic
KDIR ?= /lib/modules/$(shell uname -r)/build

all:
	$(MAKE) -C $(KDIR) M=$(CURDIR) modules

clean:
	$(MAKE) -C $(KDIR) M=$(CURDIR) clean
