.PHONY: build run clean

build:
	python3 src/pycocks/setup.py build

run:
	python3 src/main.py start

clean:
	rm -rf data/client/*
	rm -rf data/server/*
	rm -rf data/message/*
