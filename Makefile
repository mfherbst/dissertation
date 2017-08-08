all: pdf pdfa

build/CMakeCache.txt:
	mkdir build && cd build && cmake ..

build_png/CMakeCache.txt:
	mkdir build_png && cd build_png && cmake -DIMAGE_FORMAT=png ..

pdf: build/CMakeCache.txt
	cd build && make pdf

pdfa: build_png/CMakeCache.txt
	cd build_png && make pdf
