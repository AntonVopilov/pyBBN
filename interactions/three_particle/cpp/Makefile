COMPILER ?= c++
PYTHON ?= python3
all: integral.so

integral.so: integral.cpp integral.h
	$(COMPILER) -fopenmp -fPIC -shared -o integral.so integral.cpp -O4 -ffast-math -march=native -g -std=c++11 -I pybind11/include \
	`$(PYTHON)-config --cflags --ldflags` -lgsl -lgslcblas -lm -Wfatal-errors \

clean:
	rm -rf *.o *.so *.c *.so.DSYM
