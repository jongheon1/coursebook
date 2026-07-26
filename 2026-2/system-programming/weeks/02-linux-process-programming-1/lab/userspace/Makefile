CC      ?= cc
CFLAGS  ?= -Wall -Wextra -O2

PROGS = fork_exec_wait cow_observe clone_flags

all: $(PROGS)

%: %.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(PROGS)

.PHONY: all clean
