INC=-I./cutest -I/var/engine/engine -I/var/nginx/nginx-1.19.3/src/core -I/var/nginx/nginx-1.19.3/src/http -I/var/nginx/nginx-1.19.3/objs -I/var/nginx/nginx-1.19.3/src/os/unix -I/var/nginx/nginx-1.19.3/src/event -I/var/nginx/nginx-1.19.3/src/http/modules

alltests: alltests.o test_engine_pin.o CuTest.o engine_pin.o
	gcc -o alltests alltests.o test_engine_pin.o CuTest.o engine_pin.o

alltests.o: alltests.c
	gcc -c -Wall $(INC) alltests.c

test_engine_pin.o: test_engine_pin.c
	gcc -c -Wall $(INC) test_engine_pin.c

CuTest.o: cutest/CuTest.c
	gcc -c -Wall $(INC) cutest/CuTest.c

engine_pin.o: ../../engine/engine_pin.c
	gcc -c -Wall $(INC) ../../engine/engine_pin.c
