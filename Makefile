all: pdf pdfa

cmake/UseLATEX/CMakeLists.txt:
	git submodule update --init

build/CMakeCache.txt: cmake/UseLATEX/CMakeLists.txt
	mkdir build && cd build && cmake ..

build_png/CMakeCache.txt: cmake/UseLATEX/CMakeLists.txt
	mkdir build_png && cd build_png && cmake -DIMAGE_FORMAT=png ..

pdf: build/CMakeCache.txt
	cd build && make pdf

pdfa: build_png/CMakeCache.txt
	cd build_png && make pdf
