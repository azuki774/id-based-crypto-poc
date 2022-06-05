.PHONY: run

run:
	python3 src/main.py

clean:
	rm -rf data/client/*
	rm -rf data/server/*
	rm -rf data/message/*
