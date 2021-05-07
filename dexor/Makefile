CXX=g++
CXXFLAGS=-std=c++17 -ggdb -Wall -Wfatal-errors -Wpedantic
LIBS=-lncurses
BIN=dexor

dexor: dexor.o base64.o
	$(CXX) -o dexor dexor.o base64.o $(LIBS)

.PHONY: clean objclean

clean:
	rm -f *.o $(BIN)

objclean:
	rm -f *.o

