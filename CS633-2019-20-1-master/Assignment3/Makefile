CC      = mpiicc
COPT    = -g -O3
C       = mpicc

LD      = $(CC)
LE      = $(C)
LDFLAGS = $(COPT)

hpc: src.x
cse: src.a

%.x: %.o src.o
	$(LD) $(LDFLAGS) $< -o $@

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

%.a: %.o src.o
	$(LE) $(LDFLAGS) $< -o $@
clean:
	rm *.o *.x *.a
