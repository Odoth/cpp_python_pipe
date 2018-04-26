CC      := gcc 

SRC_DIR := src
OBJ_DIR := obj
BIN_DIR := bin

WARN    = -pedantic -Wall -pedantic -Wall -Wextra -Wcast-align -Wcast-qual -Wctor-dtor-privacy \
	-Wdisabled-optimization -Wformat=2 -Winit-self -Wlogical-op -Wmissing-declarations \
	-Wold-style-cast -Woverloaded-virtual -Wredundant-decls -Wshadow \
	-Wsign-conversion -Wsign-promo -Wstrict-null-sentinel -Wstrict-overflow=5 \
	-Wswitch-default -Wundef -Wno-unused-parameter -Weffc++ -Werror
C_FLAGS = -ggdb $(WARN) -std=c++11
L_FLAGS = -lstdc++

OBJ_FILES := $(patsubst %.cpp,$(OBJ_DIR)/%.o, \
	main.cpp )

.PHONY: all
all: main

.PHONY: main
main: $(BIN_DIR)/main
$(BIN_DIR)/main: $(OBJ_FILES) | $(BIN_DIR)
	$(CC) -o $(BIN_DIR)/main $(OBJ_FILES) $(L_FLAGS)

.PHONY: run
run: $(BIN_DIR)/main
	$(BIN_DIR)/main


$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp | $(OBJ_DIR)
	$(CC) -c $(C_FLAGS) -o $@ $<


$(OBJ_DIR) $(BIN_DIR):
	mkdir -p $@

.PHONY: clean
clean:
	rm -f $(OBJ_DIR)/*.o && rm -f $(BIN_DIR)/main
