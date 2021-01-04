INC=-I./cutest -I../../engine

alltests: alltests.o test_engine_pin.o CuTest.o
	gcc -o alltests alltests.o test_engine_pin.o CuTest.o

alltests.o: alltests.c
	gcc -c -Wall $(INC) alltests.c

test_engine_pin.o: test_engine_pin.c
	gcc -c -Wall $(INC) test_engine_pin.c

CuTest.o: cutest/CuTest.c
	gcc -c -Wall $(INC) cutest/CuTest.c
