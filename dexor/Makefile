CXX=g++
CXXFLAGS=-std=c++17 -ggdb -Wall -Wfatal-errors -Wpedantic
LIBS=-lncurses
BIN=dexor
OBJS=dexor.o base64.o freq.o

dexor: $(OBJS)
	$(CXX) -o $(BIN) $(OBJS) $(LIBS)

freq_gen: freq_gen.o
	$(CXX) -o freq_gen freq_gen.o

.PHONY: clean objclean

clean:
	rm -f $(OBJS) $(BIN)

objclean:
	rm -f $(OBJS)

